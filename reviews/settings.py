import os
import gspread
from pathlib import Path
from oauth2client.service_account import ServiceAccountCredentials

from reviews import environment_variables


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = environment_variables.SECRET_KEY

DEBUG = environment_variables.DEBUG

ALLOWED_HOSTS = environment_variables.ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    "main.apps.MainConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "django_celery_results",
    "django_celery_beat",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "reviews.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "reviews.wsgi.application"

ADMINS = environment_variables.ADMINS

TRACKING_MESSAGE = environment_variables.TRACKING_MESSAGE

TRACKINGLIST_CLEANUP_INTERVAL = environment_variables.TRACKINGLIST_CLEANUP_INTERVAL

THIRD_PARTY_URL = environment_variables.THIRD_PARTY_URL

EZIFY_URL = environment_variables.EZIFY_URL

EZIFY_MESSAGE = environment_variables.EZIFY_MESSAGE

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": 5432,
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"


# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# CORS configurations

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Celery Settings

CELERY_BROKER_URL = os.environ.get("REDIS_HOST")

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Kolkata"

CELERY_RESULT_BACKEND = "django-db"

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"


# Google Sheets API Configuration

GOOGLE_SHEETS_CLIENT = gspread.authorize(
    ServiceAccountCredentials.from_json_keyfile_name(
        os.path.join(BASE_DIR, environment_variables.CRED_PATH),
        environment_variables.GOOGLE_SCOPES,
    )
)

ORDER_SHEET_NAME = environment_variables.ORDER_SHEET_NAME
REVIEW_SHEET_NAME = environment_variables.REVIEW_SHEET_NAME

DATABASE_SYNC_PRODUCT_ID_WIH_SKU_INTERVAL = (
    environment_variables.DATABASE_SYNC_PRODUCT_ID_WIH_SKU_INTERVAL
)

# SHEET_ORDERS = GOOGLE_SHEETS_CLIENT.open(environment_variables.ORDER_SHEET_NAME)
# SHEET_REVIEWS = GOOGLE_SHEETS_CLIENT.open(environment_variables.REVIEW_SHEET_NAME)
