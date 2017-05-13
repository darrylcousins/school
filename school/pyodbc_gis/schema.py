__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import logging

from django.contrib.gis.db.models.fields import GeometryField
from django.db.utils import OperationalError

from sql_server.pyodbc.schema import DatabaseSchemaEditor

logger = logging.getLogger('django.contrib.gis')

class MSSqlSchemaEditor(DatabaseSchemaEditor):
    """
    This class encapsulates all backend-specific differences that pertain to
    database *creation*, such as the column types to use for particular Django
    Fields, the SQL used to create and destroy tables, and the creation and
    destruction of test databases.
    """
    sql_add_spatial_index = 'CREATE SPATIAL INDEX %(index)s ON %(table)s(%(column)s) USING '\
                            'GEOMETRY_AUTO_GRID WITH BOUNDING_BOX = %(extent)s'
    sql_add_constraint = 'ALTER TABLE %(table)s ADD CONSTRAINT %(constraint)s CHECK '\
                        '( %(column)s.STGeometryType() = \'%(geom_type)s\')'

    sql_drop_spatial_index = 'DROP INDEX %(index)s ON %(table)s'

    def __init__(self, *args, **kwargs):
        super(MSQLSchemaEditor, self).__init__(*args, **kwargs)
        self.index_sql = []
        self.constraint_sql = []

    def skip_default(self, field):
        return (
            super(MSSqlSchemaEditor, self).skip_default(field) or
            # Geometry fields can't have defaults. - TODO true?
            isinstance(field, GeometryField)
        )

    def column_sql(self, model, field, include_default=False):
        column_sql = super(MSQLSchemaEditor, self).column_sql(model, field, include_default)
        if isinstance(field, GeometryField) and field.spatial_index and not field.null:
            qn = self.connection.ops.quote_name
            db_table = model._meta.db_table

            constraint = 'chk_%s_%s_%s' % \
                              (db_table, field.column, field.geom_type)

            # Geometry-type constraint:
            self.constraint_sql.append(
                self.sql_add_constraint % {
                    'table': qn(db_table),
                    'column': qn(field.column),
                    'constraint': constraint,
                    'geom_type': geom_type,
                }
            )

            # add spatial index
            self.index_sql.append(
                self.sql_add_spatial_index % {
                    'index': qn(self._create_spatial_index_name(model, field)),
                    'table': qn(db_table),
                    'column': qn(field.column),
                    'extent': qn(field.extent),
                }
            )

        return column_sql

    def create_model(self, model):
        super(MSSqlSchemaEditor, self).create_model(model)
        self.create_constraints()
        self.create_spatial_indexes()

    def add_field(self, model, field):
        super(MSSqlSchemaEditor, self).add_field(model, field)
        self.create_constraints()
        self.create_spatial_indexes()

    def remove_field(self, model, field):
        if isinstance(field, GeometryField) and field.spatial_index:
            qn = self.connection.ops.quote_name
            sql = self.sql_drop_spatial_index % {
                'index': qn(self._create_spatial_index_name(model, field)),
                'table': qn(model._meta.db_table),
            }
            try:
                self.execute(sql)
            except OperationalError:
                logger.error(
                    "Couldn't remove spatial index: %s (may be expected "
                    "if your storage engine doesn't support them).", sql
                )

        super(MSSqlSchemaEditor, self).remove_field(model, field)

    def _create_spatial_index_name(self, model, field):
        return '%s_%s_id' % (model._meta.db_table, field.column)

    def create_spatial_indexes(self):
        for sql in self.index_sql:
            try:
                self.execute(sql)
            except OperationalError:
                logger.error(
                    "Cannot create SPATIAL INDEX %s.", sql
                )
        self.index_sql = []

    def create_constraints(self):
        for sql in self.constraint_sql:
            try:
                self.execute(sql)
            except OperationalError:
                logger.error(
                    "Cannot create CONSTRAINT %s.", sql
                )
        self.constraint_sql = []

