#!/usr/bin/env bash
set -e

echo "=============================="
echo "Starting Render build process"
echo "=============================="

# ------------------------
# Install dependencies
# ------------------------
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# ------------------------
# Apply migrations
# ------------------------
echo "Applying database migrations..."
python manage.py migrate --noinput

# ------------------------
# Collect static files
# ------------------------
echo "Collecting static files..."
python manage.py collectstatic --noinput

# ------------------------
# Create superuser from environment variables
# ------------------------
echo "Checking for superuser..."
DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin}
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@example.com}
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-password123}

# Run Django shell command to create superuser if it doesn't exist
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
username = "${DJANGO_SUPERUSER_USERNAME}"
email = "${DJANGO_SUPERUSER_EMAIL}"
password = "${DJANGO_SUPERUSER_PASSWORD}"

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser: {username}")
    User.objects.create_superuser(username=username, email=email, password=password)
else:
    print(f"Superuser {username} already exists.")
END

echo "=============================="
echo "Build process completed!"
echo "=============================="
