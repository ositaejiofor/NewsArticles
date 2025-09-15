#!/bin/bash
set -e

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser if not exists..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); \
import os; \
if not User.objects.filter(username=os.environ.get('DJANGO_SUPERUSER_USERNAME')).exists(): \
    User.objects.create_superuser(username=os.environ.get('DJANGO_SUPERUSER_USERNAME'), \
    email=os.environ.get('DJANGO_SUPERUSER_EMAIL'), \
    password=os.environ.get('DJANGO_SUPERUSER_PASSWORD'))"

echo "Build complete!"
