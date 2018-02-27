__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

"""Heroku settings and globals."""

from .production import *

import os

GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')
GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')

########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
        '127.0.0.1',
        'ellesmere.herokuapp.com',
        ]
########## END SITE CONFIGURATION

########## STATIC FILE CONFIGURATION
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))
########## END STATIC FILE CONFIGURATION

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}
########## END CACHE CONFIGURATION


