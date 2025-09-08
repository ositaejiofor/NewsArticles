#!/bin/bash

# -------------------------
# NewsPortal Windows Deployment Script
# -------------------------

echo "Starting NewsPortal deployment..."

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/Scripts/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Django development server
echo "Starting Django server on http://127.0.0.1:8000..."
start cmd /k "python manage.py runserver"

# Optional: start Celery worker
read -p "Do you want to start Celery worker? (y/n): " start_celery
if [ "$start_celery" = "y" ]; then
    echo "Starting Celery worker..."
    start cmd /k "celery -A newsportal worker -l info"
fi

echo "Deployment script finished."
