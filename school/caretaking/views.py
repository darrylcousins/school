__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.dates import DateDetailView
from django.contrib.auth.models import User
from django.contrib.gis import gdal, geos

from caretaking.models import Diary, Staff, Location

class DiaryList(ListView):
    queryset = Diary.objects.order_by('-day')
    template_name = 'diary_list.html'
    context_object_name = 'diaries'
    paginate_by = 10


class StaffDiaryList(ListView):
    template_name = 'staff_diary_list.html'
    context_object_name = 'diaries'
    paginate_by = 10

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.args[0])
        self.staff = get_object_or_404(Staff, user=self.user)
        return Diary.objects.filter(staff=self.staff).order_by('-day')

    def get_context_data(self, **kwargs):
        context = super(StaffDiaryList, self).get_context_data(**kwargs)
        context['staff'] = self.staff
        return context


class DiaryDetail(DateDetailView):
    """Present list of completed tasks for this day.

    Present map showing the completed tasks as points. Tasks are to be grouped by tasktype in order
    to be represented in different styles and points repeated are moved into a cluster of points.
    In order to do so we need to move a point by a few metres.::

        >>> from caretaking.models import Task
        >>> task = Task.objects.all()[0]
        >>> point = task.point.clone()
        >>> print(point[0])
        >>> print(point[0][0])
        >>> print(point[0][1])
        >>> point[0].set_x(point[0][0] + 0.1)
        >>> point[1].set_y(point[0][1] + 0.1)
        >>> print(point[0][0])
        >>> print(point[0][1])
        >>> print(dir(point[0]))
        >>> print(type(point[0]))
        >>> print(type(point))

    """
    date_field = 'day'
    queryset = Diary.objects.all()
    template_name = 'diary_detail.html'
    context_object_name = 'diary'
    points = []

    def get_next_point(self, point):
        if point in self.points:
            # here we want to shift the point to create a visual cluster
            value = geos.GEOSGeometry(point)
            self.points.append(value)
        else:
            value = geos.GEOSGeometry(point)
            self.points.append(value)
        return value

    def get_object(self):
        obj = super(DiaryDetail, self).get_object()
        return obj

    def get_context_data(self, **kwargs):
        context = super(DiaryDetail, self).get_context_data(**kwargs)
        context['staff'] = self.object.staff
        # get college plan for context
        # TODO add this routine as Location manager method
        try:
            value = Location.objects.get(name="CollegePlan").polygon
            context['college_wkt'] = geos.GEOSGeometry(value).wkt
        except Location.DoesNotExist:
            context['college_wkt'] = ''

        # initialize value
        value = None
        for task in self.object.tasks:
            if value is None:
                # initialize geosgeometry object
                value = self.get_next_point(task.point)
            else:
                # union of geosgeometry object is a multipoint
                value = value.union(self.get_next_point(task.point))

        # create a wkt value suitable to pass to openmaps javascript
        # TODO place this routine somewhere
        wkt = ''
        if value:
            srid = 3857
            if value.srid != srid:
                try:
                    ogr = value.ogr
                    ogr.transform(srid)
                    wkt = ogr.wkt
                except gdal.OGRException:
                    pass  # wkt left as an empty string
            else:
                wkt = value.wkt
        context['diary_wkt'] = wkt

        return context
