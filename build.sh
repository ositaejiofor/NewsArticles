#!/usr/bin/env bash
# Exit on error
set -o errexit  

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate --no-input

# (Optional) Create a superuser automatically if none exists
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser("admin", "admin@example.com", "adminpassword")
EOF
