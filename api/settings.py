"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from decouple import config
from corsheaders.defaults import default_headers

from api.utils.settings import parse_db_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-u2f8rbsoedjjz4q&tmr8(i_qk&@j-wv^6vmvrmw+&)@oyzmpzu')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)
ENVIRONMENT = config('ENVIRONMENT', default="test")

# TODO: deprecate "test", "dev" and "prod" in favor of "unittest", "development" and "production"
UNITTEST = config('TESTING', default=ENVIRONMENT == "unittest" or ENVIRONMENT == "test")
DEVELOPMENT = config('DEVELOPMENT', default=ENVIRONMENT == "development" or ENVIRONMENT == "dev")
STAGING = config('STAGING', default=ENVIRONMENT == "staging")
PRODUCTION = config('PRODUCTION', default=ENVIRONMENT == "production" or ENVIRONMENT == "prod")

DB_CONFIG = parse_db_url(url=config('DATABASE_URL', default=None))


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB', default=DB_CONFIG.get('name')),
        'USER': config('POSTGRES_USER', default=DB_CONFIG.get('user')),
        'PASSWORD': config('POSTGRES_PASSWORD', default=DB_CONFIG.get('password')),
        'HOST': config('POSTGRES_HOST', default=DB_CONFIG.get('host')),
        'PORT': config('POSTGRES_PORT', default=DB_CONFIG.get('port')),
        'TEST': {
            'NAME': config('POSTGRES_TEST_DB', default=DB_CONFIG.get('name', 'test')),
        },
        'LOGGING': {
            'version': 1,
            'loggers': {
                'djongo': {
                    'level': 'DEBUG',
                    'propagate': False,
                }
            },
        },
    }
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware' if PRODUCTION or STAGING else 'api.middleware.DisableCSRFMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.application'


# AUTH_USER_MODEL = 'core.User'


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'es-CL'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


# AWS S3

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default=None)
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default=None)
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default=None)

AWS_DEFAULT_ACL = config('AWS_DEFAULT_ACL', default='public-read')
AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL', default=(AWS_S3_REGION_NAME and "https://%s.digitaloceanspaces.com" % AWS_S3_REGION_NAME))
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

STATIC_LOCATION = config('STATIC_LOCATION', default='static')
MEDIA_LOCATION = config('MEDIA_LOCATION', default='media')
PRIVATE_MEDIA_LOCATION = config('PRIVATE_MEDIA_LOCATION', default='private')


# Static and user uploaded files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

if UNITTEST or DEVELOPMENT:
    STATIC_URL = '%s/' % STATIC_LOCATION
    STATIC_ROOT = BASE_DIR / 'staticfiles'

    MEDIA_URL = '%s/' % MEDIA_LOCATION
    MEDIA_ROOT = BASE_DIR / 'mediafiles'
else:
    STATIC_URL = '%s/%s/' % (AWS_S3_ENDPOINT_URL, STATIC_LOCATION)
    STATICFILES_STORAGE = 'api.utils.storage.StaticStorage'

    MEDIA_URL = '%s/%s/' % (AWS_S3_ENDPOINT_URL, MEDIA_LOCATION)
    DEFAULT_FILE_STORAGE = 'api.utils.storage.MediaStorage'

# STATICFILES_DIRS = (BASE_DIR / 'static', )


# Cross-Origin Resource Sharing
# https://github.com/adamchainz/django-cors-headers

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=lambda v: [s.strip() for s in v.split(',') if s and s.strip()])

if UNITTEST or DEVELOPMENT:
    CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='', cast=lambda v: [s.strip() for s in v.split(',') if s and s.strip()])
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + ['x-csrftoken']
CORS_EXPOSE_HEADERS = ['set-cookie']

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=lambda v: [s.strip() for s in v.split(',') if s and s.strip()])

SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_DOMAIN = config('SESSION_COOKIE_DOMAIN', default=None)
SESSION_COOKIE_SECURE = bool(SESSION_COOKIE_DOMAIN)

CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_DOMAIN = config('CSRF_COOKIE_DOMAIN', default=None)
CSRF_COOKIE_SECURE = bool(CSRF_COOKIE_DOMAIN)


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
