__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from sql_server.pyodbc.base import *
from sql_server.pyodbc.base import DatabaseWrapper as MSSqlDatabaseWrapper

#from .features import MSSqlFeatures
from .introspection import MSSqlIntrospection
from .operations import MSSqlOperations
from .schema import MSSqlSchemaEditor


class DatabaseWrapper(MSSqlDatabaseWrapper):
    """
    """
    SchemaEditorClass = MSSqlSchemaEditor

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        #self.features = DatabaseFeatures(self)
        self.ops = MSSqlOperations(self)
        self.introspection = MSSqlIntrospection(self)
