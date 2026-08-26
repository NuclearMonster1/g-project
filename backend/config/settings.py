"""Django settings for G Project secure file platform."""
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv(PROJECT_ROOT / ".env")

IS_VERCEL = os.getenv("VERCEL") == "1"

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-insecure-key-change-in-production")
DEBUG = os.getenv("DEBUG", "True").lower() == "true" and not IS_VERCEL

_allowed = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
_vercel_url = os.getenv("VERCEL_URL")
if _vercel_url:
    _allowed.append(_vercel_url)
ALLOWED_HOSTS = [h.strip() for h in _allowed if h.strip()]

_csrf_origins = os.getenv("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins.split(",") if o.strip()]
if IS_VERCEL and _vercel_url:
    _vercel_origin = f"https://{_vercel_url}"
    if _vercel_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(_vercel_origin)

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
    "whitenoise.middleware.WhiteNoiseMiddleware",
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

if os.getenv("DATABASE_URL"):
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=not DEBUG,
        )
    }
elif IS_VERCEL:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "/tmp/db.sqlite3",
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
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

MEDIA_ROOT = PROJECT_ROOT / os.getenv("MEDIA_ROOT", "media")
STORAGE_ROOT = PROJECT_ROOT / os.getenv("STORAGE_ROOT", "storage")

if IS_VERCEL:
    MEDIA_ROOT = Path("/tmp/media")
    STORAGE_ROOT = Path("/tmp/storage")
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

if IS_VERCEL:
    CORS_ALLOW_ALL_ORIGINS = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

LOGIN_RATE_LIMIT = int(os.getenv("LOGIN_RATE_LIMIT", "5"))

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "")
FIREBASE_AUTH_DOMAIN = os.getenv("FIREBASE_AUTH_DOMAIN", "")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "")
FIREBASE_APP_ID = os.getenv("FIREBASE_APP_ID", "")
FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET", "")
FIREBASE_MESSAGING_SENDER_ID = os.getenv("FIREBASE_MESSAGING_SENDER_ID", "")
