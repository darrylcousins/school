__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.gis.db.models.fields import GeometryField


class Location(models.Model):
    """
    Provide a location, a geospatial polygon describing a part of the school::

        >>> library = Location.objects.create(name='Library',
        ...     polygon='POLYGON ((1 1, 3 3, 3 1, 1 1))')
        >>> library.save()
        >>> print(library)
        Library
        >>> print(library.polygon)
        SRID=4326;POLYGON ((1 1, 3 3, 3 1, 1 1))

    Locate the centre of the polygon using ``STCentroid()``.

        >>> print(library.polygon.centroid)
        SRID=4326;POINT (2.33333... 1.66666...)

    """
    locationid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,
            help_text=_("Useful name for this location - by convention uses CamelCase"))
    polygon = GeometryField(
            help_text=_("Polygon or Multipolygon"))

    def __str__(self):
        "Returns the location's name."
        return self.name

    class Meta:
        ordering = ('name',)
