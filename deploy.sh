#!/bin/bash

# -------------------------
# NewsPortal Deployment Script
# -------------------------

# Set variables
PROJECT_DIR="/path/to/newsportal"   # Change this to your project path
VENV_DIR="$PROJECT_DIR/venv"
DJANGO_SETTINGS_MODULE="newsportal.settings"
GUNICORN_BIND="0.0.0.0:8000"
LOG_DIR="$PROJECT_DIR/logs"
CELERY_WORKERS=1
CELERY_BEAT=false   # Set true if using periodic tasks

echo "Starting NewsPortal deployment..."

# 1. Activate virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# 2. Navigate to project directory
cd $PROJECT_DIR

# 3. Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# 4. Run migrations
echo "Applying migrations..."
python manage.py migrate

# 5. Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 6. Create logs directory if not exists
mkdir -p $LOG_DIR

# 7. Start Gunicorn server
echo "Starting Gunicorn..."
gunicorn newsportal.wsgi:application \
    --bind $GUNICORN_BIND \
    --workers 3 \
    --log-level info \
    --access-logfile $LOG_DIR/gunicorn-access.log \
    --error-logfile $LOG_DIR/gunicorn-error.log \
    --daemon

# 8. Start Celery worker
if [ "$CELERY_WORKERS" -gt 0 ]; then
    echo "Starting Celery worker..."
    celery -A newsportal worker -l info --concurrency=$CELERY_WORKERS --detach \
        --logfile=$LOG_DIR/celery.log
fi

# 9. Start Celery beat (if using periodic tasks)
if [ "$CELERY_BEAT" = true ]; then
    echo "Starting Celery beat..."
    celery -A newsportal beat -l info --detach \
        --logfile=$LOG_DIR/celery-beat.log
fi

echo "Deployment complete!"
