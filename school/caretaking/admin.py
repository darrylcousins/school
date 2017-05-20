__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.db import models
from django.contrib import admin
from django.forms import TextInput, Textarea
from django.forms import ModelForm 
from django.utils import translation, six
from django.contrib.gis import gdal, geos
from django.contrib.gis.admin.options import GeoModelAdmin

from floppyforms.gis import BaseGeometryWidget

from .models import Staff
from .models import Location
from .models import Task
from .models import TaskType
from .models import Diary

FORMFIELD_OVERRIDES = {
    models.CharField: {'widget': TextInput(attrs={'size': '40'})},
    models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 60})},
    }

# Begin widgets
def get_wkt(value, srid=3857):
    """
    Algorithm from floppyforms.BaseGeometryWidget context_data method
    """
    if isinstance(value, six.text_type):
        try:
            value = geos.GEOSGeometry(value)
        except (geos.GEOSException, ValueError):
            value = None

    # Defaulting the WKT value to a blank string
    wkt = ''
    if value:
        if value.srid != srid:
            try:
                ogr = value.ogr
                ogr.transform(srid)
                wkt = ogr.wkt
            except gdal.OGRException:
                pass  # wkt left as an empty string
        else:
            wkt = value.wkt
    return wkt


class PolygonWidget(BaseGeometryWidget):
    """
    An OpenStreetMap widget for Location polygon objects.

    Does not allow editing of the polygon.
    """
    map_srid = 3857
    template_name = 'polygon_widget.html'
    is_polygon = True

    def __init__(self, *args, **kwargs):
        super(PolygonWidget, self).__init__(*args, **kwargs)

    def get_context(self, name, value, attrs=None, extra_context={}):
        """Get for display the college polygon"""
        context = super(PolygonWidget, self).get_context(name, value, attrs, extra_context)
        try:
            value = Location.objects.get(name="CollegePlan").polygon
            value = geos.GEOSGeometry(value)
            context['college_wkt'] = value.wkt
        except Location.DoesNotExist:
            context['college_wkt'] = ''
        return context

    class Media:
        js = (
            'https://openlayers.org/en/v4.1.0/build/ol.js',
        )
        css = {'all': ('https://openlayers.org/en/v4.1.0/css/ol.css',)}


class PointWidget(BaseGeometryWidget):
    """
    An OpenStreetMap widget for Task points.

    """
    map_srid = 3857
    template_name = 'point_widget.html'
    is_point = True
    is_collection = True

    def __init__(self, *args, **kwargs):
        super(PointWidget, self).__init__(*args, **kwargs)

    def get_context(self, name, value, attrs=None, extra_context={}):
        """Get for display the college polygon"""
        context = super(PointWidget, self).get_context(name, value, attrs, extra_context)
        try:
            value = Location.objects.get(name="CollegePlan").polygon
            value = geos.GEOSGeometry(value)
            context['college_wkt'] = value.wkt
        except Location.DoesNotExist:
            context['college_wkt'] = ''
        return context

    class Media:
        js = (
            'https://openlayers.org/en/v4.1.0/build/ol.js',
        )
        css = {'all': ('https://openlayers.org/en/v4.1.0/css/ol.css',)}
# end Widgets


class LocationAdminForm(ModelForm):
    class Meta: 
        model = Location
        fields = ['name', 'polygon']
        widgets = {
            'name': TextInput(attrs={'size': '40'}),
            'polygon': PolygonWidget()
            }


class LocationAdmin(admin.ModelAdmin): 
    form = LocationAdminForm


class TaskAdminForm(ModelForm):
    class Meta: 
        model = Task
        fields = ['description', 'point', 'completed', 'urgency', 'tasktype', 'staff']
        widgets = {
            'description': Textarea(attrs={'rows': '2', 'cols': 60}),
            'point': PointWidget()
            }


class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm


admin.site.register(Staff)
admin.site.register(Location, LocationAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskType)
admin.site.register(Diary)
