#!/bin/bash
# manage.sh - Local development runner

# Exit if any command fails
set -e

# Load .env automatically
export $(grep -v '^#' .env | xargs)

# Apply migrations
echo "Applying migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "Creating superuser if not exists..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); \
import os; \
if not User.objects.filter(username=os.environ.get('DJANGO_SUPERUSER_USERNAME')).exists(): \
    User.objects.create_superuser(username=os.environ.get('DJANGO_SUPERUSER_USERNAME'), \
    email=os.environ.get('DJANGO_SUPERUSER_EMAIL'), \
    password=os.environ.get('DJANGO_SUPERUSER_PASSWORD'))"

# Start Django server
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
