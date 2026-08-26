"""Django settings for G Project secure file platform."""
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv(PROJECT_ROOT / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-insecure-key-change-in-production")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "apps.accounts",
    "apps.files",
    "apps.scanning",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_ROOT / "frontend" / "templates"],
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [PROJECT_ROOT / "frontend" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_ROOT = PROJECT_ROOT / os.getenv("MEDIA_ROOT", "media")
STORAGE_ROOT = PROJECT_ROOT / os.getenv("STORAGE_ROOT", "storage")
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "25"))
FILE_ENCRYPTION_KEY = os.getenv("FILE_ENCRYPTION_KEY", "dev-key-must-be-32-bytes-long!!")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "login": os.getenv("LOGIN_RATE_LIMIT", "5") + "/minute",
    },
}

# No token expiry per user stories — very long lifetime
_jwt_days = int(os.getenv("JWT_ACCESS_TOKEN_LIFETIME_DAYS", "3650"))
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=_jwt_days),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=_jwt_days),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
}

SCAN_CONFIDENCE_THRESHOLD = float(os.getenv("SCAN_CONFIDENCE_THRESHOLD", "0.7"))

CORS_ALLOW_ALL_ORIGINS = DEBUG

LOGIN_RATE_LIMIT = int(os.getenv("LOGIN_RATE_LIMIT", "5"))

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "")
FIREBASE_AUTH_DOMAIN = os.getenv("FIREBASE_AUTH_DOMAIN", "")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "")
FIREBASE_APP_ID = os.getenv("FIREBASE_APP_ID", "")
FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET", "")
FIREBASE_MESSAGING_SENDER_ID = os.getenv("FIREBASE_MESSAGING_SENDER_ID", "")
