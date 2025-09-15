#!/bin/bash
set -e

echo "Starting Gunicorn..."
exec gunicorn newsportal.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --threads 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
