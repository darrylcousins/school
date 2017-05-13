pyodbc_gis
==========

Create a model with `GeometryField`::

    >>> from django.db import models
    >>> from django.contrib.gis.db.models.fields import GeometryField

    >>> class Loc(models.Model):
    ...     locid = models.AutoField(primary_key=True)
    ...     name = models.CharField(max_length=50)
    ...     geometry = GeometryField()
    ...     class Meta:
    ...         app_label = 'pyodbc_gis'

Create object with point geometry::

    >>> library = Loc(name='Library', geometry='POINT (3 4)')
    >>> print(library.name)
    Library
    >>> print(library.geometry)
    SRID=4326;POINT (3 4)

Create object with polygon geometry::

    >>> school = Loc(name='School', geometry='POLYGON ((1 1, 5 1, 5 5, 1 1))')
    >>> print(school.name)
    School
    >>> print(school.geometry)
    SRID=4326;POLYGON ((1 1, 5 1, 5 5, 1 1))

Check `within` method::

    >>> library.geometry.within(school.geometry)
    False
