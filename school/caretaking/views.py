__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import random

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
        >>> point = task.point[0].clone()
        >>> print(point.wkt)
        POINT (172.29307 -43.75858)
        >>> point.x += 0.00001
        >>> point.y += 0.00001
        >>> print(point.wkt)
        POINT (172.29308 -43.75857)

    Keep all tasks to same completed date and point::

        >>> thisday = task.completed
        >>> thispoint = task.point

    Create a bunch of tasks::

        >>> for i in range(10):
        ...     t = Task.objects.create(description=str(i),
        ...         completed=thisday,
        ...         point=thispoint)
        ...     t.save()
        ...     t.staff.add(task.staff.first())

    Set up test client::

        >>> from django.test import Client
        >>> from django.core.urlresolvers import reverse
        >>> client = Client()

    Find our diary day for this set of tasks::

        >>> diary = Diary.objects.get(day=thisday)
        >>> print(diary.get_absolute_url())
        /caretaking/diaries/2017/Mar/10/1/
        >>> response = client.get(diary.get_absolute_url())
        >>> print(response.status_code)
        200
        >>> print(len(response.context['object'].tasks))
        21
        >>> print(response.context['diary_wkt'])
        MULTIPOINT (...)


    """
    date_field = 'day'
    queryset = Diary.objects.all()
    template_name = 'diary_detail.html'
    context_object_name = 'diary'
    points = []
    targets = [t*0.00001 for t in (0, 1, 2, -1, -2)]

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
        for point in self.object.points():
            if value is None:
                # initialize geosgeometry object
                value = geos.GEOSGeometry(point)
            else:
                # union of geosgeometry object is a multipoint
                # here need to group the tasks by task type
                value = value.union(geos.GEOSGeometry(point))

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
