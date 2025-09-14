#!/usr/bin/env bash

# ------------------------
# Collect static files
# ------------------------
python manage.py collectstatic --noinput

# ------------------------
# Apply database migrations
# ------------------------
python manage.py migrate --noinput

# ------------------------
# Create superuser if it doesn't exist
# ------------------------
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(email='admin@eaglecollins.com').exists() or \
User.objects.create_superuser('admin@eaglecollins.com','admin@eaglecollins.com','AdminPass123')" \
| python manage.py shell

# ------------------------
# Start Gunicorn server
# ------------------------
gunicorn newsportal.wsgi:application --bind 0.0.0.0:$PORT
