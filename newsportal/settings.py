import os
from pathlib import Path
from dotenv import load_dotenv

# ------------------------
# Base directory
# ------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------
# Load environment variables
# ------------------------
load_dotenv(BASE_DIR / ".env")

# ------------------------
# Environment
# ------------------------
RENDER_ENV = os.getenv("RENDER_ENV", "development")  # 'production' or 'development'
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes") if RENDER_ENV == "production" else True

# ------------------------
# Hosts
# ------------------------
render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
custom_hosts = os.getenv("ALLOWED_HOSTS", "")

ALLOWED_HOSTS = []
if render_host:
    ALLOWED_HOSTS.append(render_host)
if custom_hosts:
    ALLOWED_HOSTS.extend([h.strip() for h in custom_hosts.split(",") if h.strip()])
if RENDER_ENV != "production":
    ALLOWED_HOSTS.extend(["localhost", "127.0.0.1"])

# ------------------------
# Security
# ------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-placeholder")

if RENDER_ENV == "production":
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# ------------------------
# CSRF trusted origins
# ------------------------
csrf_default = []

# Always trust Render domains
csrf_default.append("https://*.onrender.com")

# Add Render’s actual hostname if present
if render_host:
    csrf_default.append(f"https://{render_host}")

# Add custom domains from ALLOWED_HOSTS
if custom_hosts:
    for h in [h.strip() for h in custom_hosts.split(",") if h.strip()]:
        csrf_default.append(f"https://{h}")

# Local development
if RENDER_ENV != "production":
    for local in ["localhost", "127.0.0.1"]:
        csrf_default.append(f"http://{local}:8000")
        csrf_default.append(f"https://{local}:8000")

CSRF_TRUSTED_ORIGINS = csrf_default

# ------------------------
# Custom user model
# ------------------------
AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_REDIRECT_URL = "profile"

# ------------------------
# Installed apps
# ------------------------
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
    "django.contrib.sitemaps",

    # Third-party apps
    "ckeditor",
    "ckeditor_uploader",
    "crispy_forms",
    "crispy_bootstrap5",

    # Local apps
    "blog",
    "dashboard",
    "core",
    "accounts",
    "comments",
    "search",
    "composer_app",
    "notifications",
    "api",
    "ads",
    "donations",
]

CRISPY_TEMPLATE_PACK = "bootstrap5"

# ------------------------
# Middleware
# ------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ------------------------
# CKEditor settings
# ------------------------
CKEDITOR_UPLOAD_PATH = "uploads/articles/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Custom",
        "height": 400,
        "width": "100%",
        "toolbar_Custom": [
            ["Bold", "Italic", "Underline", "Strike"],
            ["NumberedList", "BulletedList", "Blockquote"],
            ["Link", "Unlink"],
            ["Image", "CodeSnippet", "Embed", "Table"],
            ["RemoveFormat", "Source"],
        ],
        "extraPlugins": ",".join(["uploadimage", "codesnippet", "embed", "autolink"]),
        "codeSnippet_theme": "monokai_sublime",
    }
}

# ------------------------
# URLs and WSGI
# ------------------------
ROOT_URLCONF = "newsportal.urls"
WSGI_APPLICATION = "newsportal.wsgi.application"

# ------------------------
# Templates
# ------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ------------------------
# Database
# ------------------------
if RENDER_ENV == "production":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ------------------------
# Password validation
# ------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------
# Internationalization
# ------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Lagos"
USE_I18N = True
USE_TZ = True

# ------------------------
# Static & Media
# ------------------------
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "mediafiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ------------------------
# Default primary key
# ------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------
# Authentication backends
# ------------------------
AUTHENTICATION_BACKENDS = [
    "accounts.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# ------------------------
# Email
# ------------------------
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend" if DEBUG else "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False") == "True"

# ------------------------
# Site framework
# ------------------------
SITE_ID = 1

# ------------------------
# Donation settings
# ------------------------
MANUAL_PAYMENT_INFO = {
    "bank_name": "OPAY",
    "account_number": "8039281188",
    "account_name": "Osita Collins Ejiofor"
}
FLW_SECRET_KEY = os.getenv("FLW_SECRET_KEY", "")
