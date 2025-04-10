import os
import datetime
from pathlib import Path
import cloudinary
import cloudinary.uploader
import cloudinary.api
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-9ym2wot9%)6k_t3m9@#7ehs=w_)ych0j!@=bebwnb@fs)ovvdb"

DEBUG = True

ALLOWED_HOSTS = ["bguess-django.onrender.com", "bguess-django-g8f5.onrender.com", "*"]

# Installed apps
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "cloudinary",
    "cloudinary_storage",
    "apps.users",
    "apps.imgtocode",
    "apps.subscriptions.apps.SubscriptionsConfig",  # Changed here to load AppConfig
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

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

WSGI_APPLICATION = "project.wsgi.application"

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://bguess_jh5d_user:lqE8QpTs1wDsFdeBArW9HSRFilRZitzi@dpg-cvdusain91rc73bc3m80-a.oregon-postgres.render.com/bguess_jh5d'
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'de8c7djwu',
    'API_KEY': '155326426895429',
    'API_SECRET': 'cgCsEB2moUSKpnP3GGSVKHkMeVY'
}
cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET'],
)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',)
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=1440),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=2),
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:1234',
    "https://bguess-django.onrender.com",
    "https://bugess.netlify.app",
]
CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:1234",
    "https://bguess-django.onrender.com",
    "https://bugess.netlify.app",
    "https://screentocode-xqu3.onrender.com"
]

# Email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = "mainbsl4@gmail.com"
EMAIL_HOST_PASSWORD = "nmwk umma atdu sosv"
EMAIL_PORT = 465
EMAIL_USE_SSL = True

# STRIPE CONFIGURATION (Live keys hardcoded)
STRIPE_MODE = "live"

STRIPE_PUBLISHABLE_KEY = "pk_live_51GSY5LH3tb3qjpqa1ieuDkGggwCy4ehrpOKFgXgQww7jW94YyWGmcphFTsODVDmfhOKDzljS4SrbnP9L8Ue7AP0600I6gNr2rf"
STRIPE_SECRET_KEY = "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"
STRIPE_WEBHOOK_SECRET = "whsec_GPzLixYE2nqGrBP7LrFsBsGfZCVv9Jwk"

STRIPE_SUCCESS_URL = "https://snipscript.ai/success"
STRIPE_CANCEL_URL = "https://snipscript.ai/cancel"

# Unfold admin styling
UNFOLD = {
    "SITE_TITLE": "Admin",
    "SITE_HEADER": "Admin",
    "SITE_SUBHEADER": "Admin",
}


# --- Render Deployment Config ---
import os

ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
