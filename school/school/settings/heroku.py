__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

"""Heroku settings and globals."""

from .production import *

import os

GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')
GDAL_LIBRARY_PATH = os.path.join(os.environ['GDAL_LIBRARY_PATH'], 'libgdal.so')

