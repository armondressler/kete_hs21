"""
Django settings for kete_hs21 project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from os import environ
from django.core.management import utils
import logging

logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
if environ.get("DJANGO_DEBUG", "false") == "true".lower():
    DEBUG = True
    SECRET_KEY = "django-insecure-=e(1cq5*00gqei$a2(u9v2g1q#9fj4^*$*s=)0shllo*6weqtd^"
else:
    DEBUG = False
    SECRET_KEY = f"django-insecure-={utils.get_random_secret_key()}"

ALLOWED_HOSTS = [
    '127.0.0.1',
    'kete-hs21.azurewebsites.net'
]

# Application definition

INSTALLED_APPS = [
    'subtitle_builder.apps.SubtitleBuilderConfig',
    'base.apps.BaseConfig',
    'course.apps.CourseConfig',
    'lesson.apps.LessonConfig',
    'accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit',
    "crispy_forms",
    "crispy_bootstrap5",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kete_hs21.urls'

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

WSGI_APPLICATION = 'kete_hs21.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'de-DE'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

#https://docs.djangoproject.com/en/3.2/topics/auth/default/#the-login-required-decorator
LOGIN_URL = "/accounts/login"

LOGIN_REDIRECT_URL = "/dashboard"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#https://github.com/django-crispy-forms/crispy-bootstrap5
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

#FFMPEG
FFMPEG_PATH = environ.get("DJANGO_FFMPEG_PATH")
if not FFMPEG_PATH:
    logger.warning("Cannot determine ffmpeg binary location, DJANGO_FFMPEG_PATH env not set")


#Media upload

MEDIA_URL = "/media/"

RECORDINGS_URL = MEDIA_URL + "recordings"

SLIDESHOWS_URL = MEDIA_URL + "slideshows"

MEDIA_ROOT = BASE_DIR / "media"

RECORDINGS_ROOT = MEDIA_ROOT / "recordings"

SLIDESHOWS_ROOT = MEDIA_ROOT / "slideshows"

import os
for media_dir in (MEDIA_ROOT, RECORDINGS_ROOT, SLIDESHOWS_ROOT):
    if not os.path.isdir(media_dir):
        logger.info(f"Creating missing MEDIA_DIRS {MEDIA_ROOT}, {RECORDINGS_ROOT}, {SLIDESHOWS_ROOT}")
        os.mkdir(media_dir)


#Azure TTS API
AZURE_BLOB_CONTAINER_URL = "https://defaultst01.blob.core.windows.net/speech-to-text-audiofiles"

AZURE_STORAGE_ACCOUNT_SAS_QUERY_STRING = environ.get("DJANGO_STORAGE_ACCOUNT_SAS_QUERY_STRING")
if not AZURE_STORAGE_ACCOUNT_SAS_QUERY_STRING:
    logger.warning("No azure TTS api key provided, DJANGO_STORAGE_ACCOUNT_SAS_QUERY_STRING env not set")

AZURE_OCP_APIM_SUBSCRIPTION_KEY = environ.get("DJANGO_OCP_APIM_SUBSCRIPTION_KEY")
if not AZURE_OCP_APIM_SUBSCRIPTION_KEY:
    logger.warning("No azure TTS api key provided, DJANGO_OCP_APIM_SUBSCRIPTION_KEY env not set")
