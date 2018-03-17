__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

"""Home settings and globals."""

from .local import *

# GDAL_LIBRARY_PATH = 'C:\\OSGeo4W\\bin\\gdal201.dll'

########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
        '127.0.0.1',
        '192.168.1.67'
        ]
########## END SITE CONFIGURATION

########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# Assign to variable to make it easier to comment out during development
DEFAULT_DB = {
    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    'NAME': 'ellesmere',
    'USER': 'ellesmere',
    'PASSWORD': 'ellesmere',
    'HOST':'127.0.0.1',
    'PORT': 5432,
}
DATABASES = {
    'default': DEFAULT_DB,
}

