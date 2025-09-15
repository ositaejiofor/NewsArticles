#!/bin/bash

# ------------------------
# Exit immediately if a command fails
# ------------------------
set -e

echo "Starting Render build script..."

# ------------------------
# Activate virtual environment (if using .venv)
# ------------------------
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# ------------------------
# Install dependencies
# ------------------------
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# ------------------------
# Run migrations
# ------------------------
echo "Running migrations..."
python manage.py migrate --noinput

# ------------------------
# Collect static files
# ------------------------
echo "Collecting static files..."
python manage.py collectstatic --noinput

# ------------------------
# Create superuser if not exists
# ------------------------
# Environment variables for superuser
DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin}
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@example.com}
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-admin123}

echo "Creating superuser..."
python manage.py shell <<END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="$DJANGO_SUPERUSER_USERNAME").exists():
    User.objects.create_superuser(
        username="$DJANGO_SUPERUSER_USERNAME",
        email="$DJANGO_SUPERUSER_EMAIL",
        password="$DJANGO_SUPERUSER_PASSWORD"
    )
END

echo "Build script completed successfully!"
