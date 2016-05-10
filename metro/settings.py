"""
Django settings for metro project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wn^c3f1tf)fqpq$46hdr#co!xez+dhjl)w2x%s-yw1ha0hy21w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

# Application definition

INSTALLED_APPS = (
    'multifilefield',
    'daterange_filter',
    'geoposition',
    'adminactions',
    'grappelli_dynamic_navbar',
    'ajax_select',
    'grappelli',
    'import_export',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'metropolitana',
    'digitalizacion',
    'movil',
    'verificaciones',
    'cartera',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'apptemplates.Loader',
#     'django.template.loaders.eggs.Loader',
)


ROOT_URLCONF = 'metro.urls'

WSGI_APPLICATION = 'metro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default_': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'dd0lkll4l2717a',
    'USER': 'rsujiklxazuzbo',
    'PASSWORD': 'abxYG-a0IR84FV-7zL57a1BgP4',
    'HOST': 'ec2-54-235-83-5.compute-1.amazonaws.com',
    'PORT': '5432',
},
'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'django',
    'USER': 'postgres',
    'USER': 'postgres',
    'PASSWORD': 'postgres',
    'HOST': 'localhost',
    'PORT': '5432',
}
}
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es-NI'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

import django.conf.global_settings as DEFAULT_SETTINGS

CUSTOM_PROCESSORS = ('django.core.context_processors.request',)

TEMPLATE_CONTEXT_PROCESSORS = \
DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + CUSTOM_PROCESSORS


RUTA_PROYECTO = os.path.dirname(os.path.realpath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'


SESSION_COOKIE_AGE = 7200
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
