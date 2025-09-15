#!/bin/bash
set -e

# -------------------------
# Render Start Command
# -------------------------

# Apply database migrations
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

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn newsportal.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --threads 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
