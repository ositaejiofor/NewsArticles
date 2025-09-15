#!/bin/bash

# ==============================
# CONFIG - EDIT THESE VALUES
# ==============================
GITHUB_USER="yourgithubusername"
GITHUB_REPO="newsportal"
RENDER_SERVICE_NAME="newsportal"
RENDER_ENV="python-3.13"
DJANGO_SECRET_KEY="replace_with_your_secret_key"
ALLOWED_HOSTS=".eaglecollins.com"
DATABASE_URL="replace_with_render_postgres_url"
FLW_SECRET_KEY="replace_with_flutterwave_key"
SUPERUSER_NAME="admin"
SUPERUSER_EMAIL="admin@eaglecollins.com"
SUPERUSER_PASS="yourpassword"
ROOT_DIR=""   # leave empty if manage.py is at repo root
CUSTOM_DOMAIN="www.eaglecollins.com"
APEX_DOMAIN="eaglecollins.com"

# Cloudflare config
CF_API_TOKEN="your_cloudflare_api_token"
CF_ZONE_ID="your_cloudflare_zone_id"

RENDER_CLI_PATH=$(which render)
SLEEP_INTERVAL=10
SSL_RETRIES=30
SSL_WAIT=10

# ==============================
# 1. Git setup
# ==============================
echo "=== Git Setup ==="
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial deploy"
    git branch -M main
    git remote add origin https://github.com/$GITHUB_USER/$GITHUB_REPO.git
    git push -u origin main
else
    echo "Git repo exists. Pushing latest changes..."
    git add .
    git commit -m "Update for deployment" || echo "No changes to commit."
    git push origin main
fi

# ==============================
# 2. Create build.sh
# ==============================
echo "=== Creating build.sh ==="
cat <<EOL > build.sh
#!/bin/bash
pip install -r requirements.txt
python manage.py migrate --noinput
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(email='\$DJANGO_SUPERUSER_EMAIL').exists() or \
User.objects.create_superuser('\$DJANGO_SUPERUSER_USERNAME','\$DJANGO_SUPERUSER_EMAIL','\$DJANGO_SUPERUSER_PASSWORD')" | python manage.py shell
EOL
chmod +x build.sh

# ==============================
# 3. Render CLI: Create or Update Service
# ==============================
echo "=== Checking Render service ==="
EXISTS=$($RENDER_CLI_PATH services list | grep -w $RENDER_SERVICE_NAME || echo "")

if [ -z "$EXISTS" ]; then
    echo "Render service not found. Creating new service..."
    $RENDER_CLI_PATH services create web \
      --name $RENDER_SERVICE_NAME \
      --repo https://github.com/$GITHUB_USER/$GITHUB_REPO.git \
      --branch main \
      --root-dir "$ROOT_DIR" \
      --build-command "./build.sh" \
      --start-command "gunicorn newsportal.wsgi:application --bind 0.0.0.0:\$PORT" \
      --env $RENDER_ENV \
      --auto-deploy
else
    echo "Render service exists. Updating build and start commands..."
    $RENDER_CLI_PATH services update $RENDER_SERVICE_NAME \
      --build-command "./build.sh" \
      --start-command "gunicorn newsportal.wsgi:application --bind 0.0.0.0:\$PORT"
fi

# ==============================
# 4. Set environment variables
# ==============================
echo "=== Setting environment variables on Render ==="
declare -A env_vars=(
    ["DEBUG"]="False"
    ["SECRET_KEY"]="$DJANGO_SECRET_KEY"
    ["ALLOWED_HOSTS"]="$ALLOWED_HOSTS"
    ["DATABASE_URL"]="$DATABASE_URL"
    ["FLW_SECRET_KEY"]="$FLW_SECRET_KEY"
    ["DJANGO_SUPERUSER_USERNAME"]="$SUPERUSER_NAME"
    ["DJANGO_SUPERUSER_EMAIL"]="$SUPERUSER_EMAIL"
    ["DJANGO_SUPERUSER_PASSWORD"]="$SUPERUSER_PASS"
)

for key in "${!env_vars[@]}"; do
    $RENDER_CLI_PATH env set $RENDER_SERVICE_NAME $key "${env_vars[$key]}"
done

# ==============================
# 5. Wait for Render build
# ==============================
echo "=== Waiting for Render service to go live ==="
while true; do
    STATUS=$($RENDER_CLI_PATH services list | grep $RENDER_SERVICE_NAME | awk '{print $3}')
    if [[ "$STATUS" == "Live" ]]; then
        echo "Render service is live!"
        break
    else
        echo "Current status: $STATUS. Waiting $SLEEP_INTERVAL seconds..."
        sleep $SLEEP_INTERVAL
    fi
done

# ==============================
# 6. Create Cloudflare CNAME for www
# ==============================
echo "=== Configuring Cloudflare DNS for $CUSTOM_DOMAIN ==="
CF_CHECK=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records?type=CNAME&name=$CUSTOM_DOMAIN" \
    -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" | jq -r '.result | length')

if [ "$CF_CHECK" -eq 0 ]; then
    curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
        -H "Authorization: Bearer $CF_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data "{\"type\":\"CNAME\",\"name\":\"$CUSTOM_DOMAIN\",\"content\":\"$RENDER_SERVICE_NAME.onrender.com\",\"ttl\":120,\"proxied\":false}" \
        | jq
    echo "✅ Cloudflare CNAME record created for $CUSTOM_DOMAIN"
else
    echo "⚠️ Cloudflare CNAME already exists for $CUSTOM_DOMAIN"
fi

# ==============================
# 7. Create Page Rule for apex redirect
# ==============================
echo "=== Creating Cloudflare Page Rule to redirect $APEX_DOMAIN → $CUSTOM_DOMAIN ==="
PAGE_RULE_CHECK=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/pagerules" \
    -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" | jq -r ".result[] | select(.targets[].constraint.value==\"$APEX_DOMAIN/*\") | .id")

if [ -z "$PAGE_RULE_CHECK" ]; then
    curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/pagerules" \
        -H "Authorization: Bearer $CF_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data "{\"targets\":[{\"target\":\"url\",\"constraint\":{\"operator\":\"matches\",\"value\":\"$APEX_DOMAIN/*\"}}],\"actions\":[{\"id\":\"forwarding_url\",\"value\":{\"url\":\"https://$CUSTOM_DOMAIN/\$1\",\"status_code\":301}}],\"priority\":1,\"status\":\"active\"}" \
        | jq
    echo "✅ Page Rule created: $APEX_DOMAIN → $CUSTOM_DOMAIN"
else
    echo "⚠️ Page Rule already exists for apex domain redirect"
fi

# ==============================
# 8. Wait for DNS propagation
# ==============================
echo "=== Waiting for DNS propagation ==="
while true; do
    IP=$(dig +short $CUSTOM_DOMAIN)
    if [ -n "$IP" ]; then
        echo "DNS resolved to $IP"
        break
    else
        echo "DNS not propagated yet. Waiting 10s..."
        sleep 10
    fi
done

# ==============================
# 9. Verify HTTPS on www and apex
# ==============================
echo "=== Verifying HTTPS for $CUSTOM_DOMAIN and $APEX_DOMAIN ==="
for i in $(seq 1 $SSL_RETRIES); do
    HTTP_STATUS_WWW=$(curl -o /dev/null -s -w "%{http_code}" https://$CUSTOM_DOMAIN || echo "")
    HTTP_STATUS_APEX=$(curl -o /dev/null -s -w "%{http_code}" https://$APEX_DOMAIN || echo "")

    if [ "$HTTP_STATUS_WWW" == "200" ] && [ "$HTTP_STATUS_APEX" == "301" ]; then
        echo "✅ HTTPS verified! $CUSTOM_DOMAIN is live and $APEX_DOMAIN redirects correctly."
        break
    else
        echo "Waiting for SSL to propagate... Retry $i/$SSL_RETRIES"
        sleep $SSL_WAIT
    fi
done

echo "===================================================="
echo "Deployment complete. Your Django site is fully live with HTTPS!"
echo "Render default domain: https://$RENDER_SERVICE_NAME.onrender.com"
echo "Custom domain: https://$CUSTOM_DOMAIN (apex redirects automatically to www)"
echo "===================================================="
