"""
Django settings for varosha project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
import json
import dj_database_url
from os import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cw$l56sz_qj0p(wv*_)hm305)q_zoke2xm$@8fxcz(dbaaz2(!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [".awsapprunner.com","127.0.0.1",".railway.app"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'sorl.thumbnail',
    'varosha'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'varosha.urls'

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

WSGI_APPLICATION = 'varosha.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if "DATABASE_SECRET" in environ:
    database_secret = environ.get("DATABASE_SECRET")
    db_url = database_secret
    DATABASES = {"default": dj_database_url.parse(db_url)}
else:
    DATABASES = {"default": dj_database_url.parse("sqlite:///db.sqlite3")}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

TIME_ZONE = 'UTC'


USE_I18N = True
USE_L10N = True

# Set the default language, or use LANGUAGE_CODE to specify your default language
LANGUAGE_CODE = 'el-gr'

# Define available languages
LANGUAGES = [
    ('el', 'Ελληνικά'),
    ('en', 'English'),
]


LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = 'static/'

MEDIA_URL = "https://varosha-media.s3.amazonaws.com/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = ['https://6zytaqhsqx.us-east-1.awsapprunner.com','https://varoshadjango-production.up.railway.app']

if "AWS_SECRET_ACCESS_KEY" in environ:
    AWS_ACCESS_KEY_ID = environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = environ.get("AWS_SECRET_ACCESS_KEY")
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    THUMBNAIL_STORAGE = DEFAULT_FILE_STORAGE
    AWS_STORAGE_BUCKET_NAME = 'varosha-media'
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_S3_REGION_NAME = 'us-east-1'
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

if "GOOGLE_API_KEY" in environ:
    GOOGLE_API_KEY = environ.get("GOOGLE_API_KEY")
else:
    GOOGLE_API_KEY = None

if "SUPER_USER_PASS" in environ:
    SUPER_USER_PASS = environ.get("SUPER_USER_PASS")
else:
    SUPER_USER_PASS = "dev-admin-pass"

if "MAIL_PASS" in environ:
    MAIL_PASS = environ.get("SUPER_USER_PASS")
else:
    MAIL_PASS = ""

THUMBNAIL_DEBUG=True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['console', 'file']
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'varosha': {  # Replace 'myapp' with your app name
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
