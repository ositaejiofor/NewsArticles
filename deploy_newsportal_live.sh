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
RENDER_CLI_PATH=$(which render)  # assumes render CLI is installed

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
echo "=== Waiting for Render build to finish ==="
while true; do
    STATUS=$($RENDER_CLI_PATH services list | grep $RENDER_SERVICE_NAME | awk '{print $3}')
    if [[ "$STATUS" == "Live" ]]; then
        echo "Render service is live!"
        break
    else
        echo "Current status: $STATUS. Waiting 10s..."
        sleep 10
    fi
done

# ==============================
# 6. Check site live
# ==============================
SITE_URL="https://$RENDER_SERVICE_NAME.onrender.com"
HTTP_STATUS=$(curl -o /dev/null -s -w "%{http_code}\n" $SITE_URL)
if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "✅ Site is live: $SITE_URL"
else
    echo "⚠️ Site may not be live yet. Status code: $HTTP_STATUS"
fi

# ==============================
# 7. Cloudflare DNS instructions
# ==============================
echo "===================================================="
echo "Cloudflare DNS settings:"
echo "Type: CNAME"
echo "Name: www"
echo "Target: $RENDER_SERVICE_NAME.onrender.com"
echo "Proxy: DNS only (gray cloud)"
echo ""
echo "Optional: redirect apex domain to www via Page Rule:"
echo "https://eaglecollins.com/* → https://www.eaglecollins.com/\$1"
echo "===================================================="
