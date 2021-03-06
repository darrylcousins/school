__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

"""Heroku settings and globals."""

import dj_database_url
from .production import *

import os

# os.environ variables set by heroku fail - is $HOME set correctly on server?
#GDAL_LIBRARY_PATH = '/app/.heroku/vendor/lib/libgdal.so'
#GEOS_LIBRARY_PATH = '/app/.heroku/vendor/lib/libgeos_c.so'
# trying with my own fork of buildpack
GDAL_LIBRARY_PATH = os.getenv(
        'GDAL_LIBRARY_PATH',
        '/app/.heroku/vendor/lib/libgdal.so')
GEOS_LIBRARY_PATH = os.getenv(
        'GEOS_LIBRARY_PATH',
        '/app/.heroku/vendor/lib/libgeos_c.so')


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False


# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = 'https://s3.us-east-2.amazonaws.com/cousinsd-ellesmere-static/assets/'


########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
        '127.0.0.1',
        'ellesmere.herokuapp.com',
        ]
########## END SITE CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES['default'] =  dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
########## END DATABASE CONFIGURATION


