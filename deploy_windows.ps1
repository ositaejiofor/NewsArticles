# -------------------------
# NewsPortal Windows Deployment Script (PowerShell)
# -------------------------

Write-Host "Starting NewsPortal deployment..." -ForegroundColor Cyan

# Activate virtual environment
Write-Host "Activating virtual environment..."
& ".\venv\Scripts\Activate.ps1"

# Install/update dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Apply migrations
Write-Host "Applying migrations..."
python manage.py migrate

# Collect static files
Write-Host "Collecting static files..."
python manage.py collectstatic --noinput

# Start Django development server
Write-Host "Starting Django server on http://127.0.0.1:8000..."
Start-Process powershell -ArgumentList "python manage.py runserver"

# Optional: start Celery worker
$startCelery = Read-Host "Do you want to start Celery worker? (y/n)"
if ($startCelery -eq "y") {
    Write-Host "Starting Celery worker..."
    Start-Process powershell -ArgumentList "celery -A newsportal worker -l info"
}

Write-Host "Deployment script finished." -ForegroundColor Green
