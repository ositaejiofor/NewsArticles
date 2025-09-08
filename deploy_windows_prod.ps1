# -------------------------
# NewsPortal Production-like Deployment Script (Windows)
# -------------------------

$ProjectPath = "C:\Users\TOSHIBA\Desktop\NewsArticles"  # Change to your path
$VenvPath = "$ProjectPath\venv"
$LogPath = "$ProjectPath\logs"
$SSLPath = "$ProjectPath\ssl"

# Create logs folder if not exists
if (-not (Test-Path $LogPath)) { New-Item -ItemType Directory -Path $LogPath }

Write-Host "Starting NewsPortal deployment..." -ForegroundColor Cyan

# Activate virtual environment
Write-Host "Activating virtual environment..."
& "$VenvPath\Scripts\Activate.ps1"

# Pull latest code from Git
if (Test-Path "$ProjectPath\.git") {
    Write-Host "Pulling latest code from Git..."
    Set-Location $ProjectPath
    git pull origin main
}

# Install/update dependencies
Write-Host "Installing dependencies..."
pip install -r "$ProjectPath\requirements.txt"

# Apply migrations
Write-Host "Applying migrations..."
python "$ProjectPath\manage.py" migrate

# Collect static files
Write-Host "Collecting static files..."
python "$ProjectPath\manage.py" collectstatic --noinput

# Start Django server with HTTPS
$DjangoLog = "$LogPath\django.log"
Start-Process powershell -ArgumentList "python `"$ProjectPath\manage.py`" runserver_plus --cert-file `"$SSLPath\localhost.crt`" 0.0.0.0:8000 *> `"$DjangoLog`"" -WindowStyle Normal

# Start Celery worker (optional)
$startCelery = Read-Host "Do you want to start Celery worker? (y/n)"
if ($startCelery -eq "y") {
    $CeleryLog = "$LogPath\celery.log"
    Start-Process powershell -ArgumentList "celery -A newsportal worker -l info *> `"$CeleryLog`"" -WindowStyle Normal
}

# Start Celery beat (optional)
$startBeat = Read-Host "Do you want to start Celery beat (scheduled tasks)? (y/n)"
if ($startBeat -eq "y") {
    $BeatLog = "$LogPath\celery-beat.log"
    Start-Process powershell -ArgumentList "celery -A newsportal beat -l info *> `"$BeatLog`"" -WindowStyle Normal
}

Write-Host "Deployment finished!" -ForegroundColor Green
Write-Host "Check logs in $LogPath for server output."
