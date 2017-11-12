# -*- coding: utf-8 -*-

"""
Django settings for yurasic project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from utils.try_get_env import try_get_env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check_if_on_heroku():
    ENV_ON_HEROKU = 'ON_HEROKU'
    if ENV_ON_HEROKU in os.environ:
        return True
    return False


ON_HEROKU = check_if_on_heroku()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# Get ENV in local usecase
try_get_env('.env.yaml')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['YURASIC_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'yurasic.herokuapp.com',
    '127.0.0.1'
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',

    'haystack',

    'songsapp.apps.SongsappConfig',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'yurasic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            # 'environment': 'yurasic.jinja2.environment',
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'yurasic.wsgi.application'


###############################################################################
# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
###############################################################################

def get_database_url():
    import urllib.parse as urlparse
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    return url


if ON_HEROKU:
    print("Init Database on heroku")
    database_url = get_database_url()
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': database_url.path[1:],
            'USER': database_url.username,
            'PASSWORD': database_url.password,
            'HOST': database_url.hostname,
            'PORT': database_url.port,
        }
    }
else:
    print("Init Database on local")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'yurasic',
            'USER': 'yurasic_user',
            'PASSWORD': '12345',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# Update database configuration with $DATABASE_URL.
import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=500)
for k,v in db_from_env.items():
    # not None and not empty
    if v:
        DATABASES['default'][k] = v

print(DATABASES)

###############################################################################
# Elasticsearch and haystack
###############################################################################

import urllib.parse as urlparse

ES_URL = urlparse.urlparse(os.environ.get('BONSAI_URL') or 'http://127.0.0.1:9200/')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': ES_URL.scheme + '://' + ES_URL.hostname + ':443',
        'INDEX_NAME': 'haystack',
    },
}
if ES_URL.username:
    HAYSTACK_CONNECTIONS['default']['KWARGS'] = \
        {"http_auth": ES_URL.username + ':' + ES_URL.password}

###############################################################################
#
###############################################################################

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

# TODO maybe you are too strict???
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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIR = [
    os.path.join(BASE_DIR, "static")
]

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
