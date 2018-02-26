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
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = normpath(join(SITE_ROOT, 'staticfiles'))
########## END STATIC FILE CONFIGURATION
