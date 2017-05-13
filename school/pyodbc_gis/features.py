__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.contrib.gis.db.backends.base.features import BaseSpatialFeatures
from sql_server.pyodbc.features import DatabaseFeatures as MSSqlDatabaseFeatures


class DatabaseFeatures(BaseSpatialFeatures, MSSqlDatabaseFeatures):
    supports_3d_storage = True
    supports_3d_functions = True
    supports_left_right_lookups = True

