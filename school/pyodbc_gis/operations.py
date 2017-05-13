__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.contrib.gis.db.backends.base.operations import BaseSpatialOperations
from django.contrib.gis.db.backends.utils import SpatialOperator
from django.contrib.gis.db.models import GeometryField, aggregates
from django.utils.functional import cached_property

from sql_server.pyodbc.operations import DatabaseOperations


class MSSqlBoolMethod(SpatialOperator):
    """SQL Server (non-static) spatial functions are treated as methods,
    for eg g.STContains(p)"""

    sql_template = '%(geo_col)s.%(func)s(%(geometry)s) = 1'

    def __init__(self, function, **kwargs):
        super(MSSqlBoolMethod, self).__init__(func=function, **kwargs)


class MSSqlDistanceFunc(SpatialOperator):
    """Implements distance comparison lookups, eg distance_lte"""

    sql_template = ('%(geo_col)s.%(func)s(%(geometry)s) '
                    '%(op)s %(result)s')

    def __init__(self, op):
        super(MSSqlDistanceFunc, self).__init__(func='STDistance',
                                                op=op)

    def as_sql(self, connection, lookup, template_params, sql_params):
        template_params.update({'result': '%s'})
        return super(MSSqlDistanceFunc, self).__init__(connection, lookup, template_params, sql_params)


class MSSqlBBBoolMethod(MSSqlBoolMethod):
    """SQL Server has no native bounding-box methods, but we can emulate
    them with a slightly more complicated expression.  The call will
    be translated into something like
    col.STEnvelope().STOverlaps(geom.STEnvelope())
    where STEnvelope() first simplifies the geometries to their
    bounding rectangles."""

    sql_template = '%(geo_col)s.STEnvelope().%(function)s(%(geometry)s.STEnvelope()) = 1'

    def __init__(self, func):
        super(MSSqlBoolMethod, self).__init__(func=func)


class MSSqlAdapter(str):
    """This adapter works around an apparent bug in the pyodbc driver
    itself.  We only require the wkt adapter, but if we use
    django.contrib.gis.db.backends.adapter.WKTAdapter then
    cursor.execute() fails because it doesn't call str() on unrecognised
    types.  So we make sure that our adaper *is* a string."""

    def __new__(cls, geom):
        geostr = str.__new__(cls, geom.wkt)
        geostr.srid = geom.srid
        return geostr

    def __eq__(self, other):
        if not isinstance(other, MSSqlAdapter):
            return False
        return super(MSSqlAdapter, self).__eq__(other) and \
            self.srid == other.srid

    def prepare_database_save(self, unused):
        return self


class MSSqlOperations(BaseSpatialOperations, DatabaseOperations):
    """
    """

    mssql = True
    name = 'mssql'

    # duplicated in function_names
    area = 'STArea'
    difference = 'STDifference'
    distance = 'STDifference'
    intersection = 'STIntersection'
    length = 'STLength'
    num_points = 'STNumPoints'
    union = 'STUnion'

    unsupported_functions = set()

    Adapter = MSSqlAdapter

    @cached_property
    def select(self):
        return '%s.STAsText()'

    @cached_property
    def gis_operators(self):
        geometry_functions = {
            'bbcontains': MSSqlBBBoolMethod('STContains'),
            'bboverlaps': MSSqlBBBoolMethod('STOverlaps'),
            'contained': MSSqlBBBoolMethod('STWithin'),
            'contains': MSSqlBoolMethod('STContains'),
            'crosses': MSSqlBoolMethod('STCrosses'),
            'disjoint': MSSqlBoolMethod('STDisjoint'),
            'equals': MSSqlBoolMethod('STEquals'),  # can we also implement exact, same_as like this?
            'intersects': MSSqlBoolMethod('STIntersects'),
            'overlaps': MSSqlBoolMethod('STOverlaps'),
            'touches': MSSqlBoolMethod('STTouches'),
            'within': MSSqlBoolMethod('STWithin'),
        }
        distance_functions = {
            'distance_gt': (MSSqlDistanceFunc('>'), dtypes),
            'distance_gte': (MSSqlDistanceFunc('>='), dtypes),
            'distance_lt': (MSSqlDistanceFunc('<'), dtypes),
            'distance_lte': (MSSqlDistanceFunc('<='), dtypes),
        }
        geometry_functions.update(distance_functions)

        geography_functions = {
            'contains': MSSqlBoolMethod('STContains'),
            'disjoint': MSSqlBoolMethod('STDisjoint'),
            'equals': MSSqlBoolMethod('STEquals'),
            'intersects': MSSqlBoolMethod('STIntersects'),
            'overlaps': MSSqlBoolMethod('STOverlaps'),
            'within': MSSqlBoolMethod('STWithin'),
        }
        geography_functions.update(distance_functions)

        gis_terms = set(geometry_functions) | set(['isnull'])
        return gis_terms

    @cached_property
    def function_names(self):
        return {
            'Area': 'STArea',
            'Centroid': 'STCentroid',
            'Difference': 'STDifference',
            'Distance': 'STDistance',
            'Intersection': 'STIntersection',
            'Length': 'STLength',
            'NumGeometries': 'STNumGeometries',
            'NumPoints': 'STNumPoints',
            'SymDifference': 'STSymDifference',
            'Union': 'STUnion',
        }

    # Default conversion functions for aggregates; will be overridden if implemented
    # for the spatial backend.
    def convert_extent(self, box, srid):
        raise NotImplementedError('Aggregate extent not implemented for this spatial backend.')

    def convert_extent3d(self, box, srid):
        raise NotImplementedError('Aggregate 3D extent not implemented for this spatial backend.')

    def convert_geom(self, geom_val, geom_field):
        raise NotImplementedError('Aggregate method not implemented for this spatial backend.')

    def check_expression_support(self, expression):
        if isinstance(expression, self.disallowed_aggregates):
            raise NotImplementedError(
                "%s spatial aggregation is not supported by this database backend." % expression.name
            )
        super(BaseSpatialOperations, self).check_expression_support(expression)

    def spatial_aggregate_name(self, agg_name):
        raise NotImplementedError('Aggregate support not implemented for this spatial backend.')

    def spatial_function_name(self, func_name):
        if func_name in self.unsupported_functions:
            raise NotImplementedError("This backend doesn't support the %s function." % func_name)
        return self.function_names.get(func_name, self.geom_func_prefix + func_name)

    # Routines for getting the OGC-compliant models --- SQL Server
    # does not have OGC-compliant tables
    def geometry_columns(self):
        raise NotImplementedError

    def spatial_ref_sys(self):
        raise NotImplementedError

    # GeometryField operations
    def geo_db_type(self, f):
        # We only have the one geometry type (especially since we
        # don't currently support geography):
        return 'geometry'

    def get_distance(self, f, value, lookup_type):
        """
        Returns the distance parameters for the given geometry field,
        lookup value, and lookup type.  This is based on the Spatialite
        backend, since we don't currently support geography operations.
        """
        if not value:
            return []
        value = value[0]
        if isinstance(value, Distance):
            if f.geodetic(self.connection):
                raise ValueError('The SQL Server backend does not support '
                                 'distance queries on geometry fields with '
                                 'a geodetic coordinate system. Distance '
                                 'objects; use a numeric value of your '
                                 'distance in degrees instead.')
            else:
                dist_param = getattr(value, Distance.unit_attname(f.units_name(self.connection)))
        else:
            dist_param = value
        return [dist_param]

    def get_geom_placeholder(self, f, value, compiler):
        """
        Because SQL Server does not support spatial transformations,
        there is no need to modify the placeholder based on the
        contents of the given value.  We do need to specify the SRID
        however, since this argument is required.
        """
        if hasattr(value, 'expression'):
            placeholder = self.get_expression_column(value)
            #placeholder, _ = compiler.compile(value)
        else:
            ns = 'geography' if f.geography else 'geometry'
            placeholder = '%s::STGeomFromText(%%s,%s)' % (ns, f.srid)
        return placeholder

