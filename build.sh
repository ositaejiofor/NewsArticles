#!/bin/bash
# Exit immediately if a command fails
set -e

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
from django.conf import settings; \
if not User.objects.filter(username=settings.DJANGO_SUPERUSER_USERNAME).exists(): \
    User.objects.create_superuser(settings.DJANGO_SUPERUSER_USERNAME, settings.DJANGO_SUPERUSER_EMAIL, settings.DJANGO_SUPERUSER_PASSWORD)" | python manage.py shell
