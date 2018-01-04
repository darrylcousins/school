__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import datetime
import random

from django.db.models import Sum, Count
from django.http.request import QueryDict
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.dates import DateDetailView
from django.contrib.auth.models import User
from django.contrib.gis import gdal, geos

from caretaking.models import Diary, Staff, Location, Task
from caretaking.forms import DiaryForm


class StaffList(ListView):
    model = Staff
    template_name = 'staff_list.html'


class TaskList(ListView):
    model = Task
    template_name = 'task_list.html'
    paginate_by = 30
    end_date = None
    start_date = None
    default_range = 7 # 7 days
    search_term = ''

    def get(self, request, *args, **kwargs):
        """Insert logic here before ``get_queryset`` and ``get_context_data are called.

        Figure out number of days and start date based on user input.

        Default is to make a range of the past 7 days.
        """
        start_date = self.request.GET.get('start-date', None)
        end_date = self.request.GET.get('end-date', None)

        if start_date is not None and end_date is not None:
            self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            self.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        else:
            self.end_date = datetime.datetime.today()
            self.start_date = self.end_date - datetime.timedelta(days=self.default_range)

        self.search_term = self.request.GET.get('q', '')

        return super(TaskList, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """Collect task entries for this user.

        Show particular date ranges: past week, past month, past year.

        Also filter by a search term which will highlight tasks containing the search term.
        """
        self.user = get_object_or_404(User, username=self.kwargs.get('username'))
        self.staff = get_object_or_404(Staff, user=self.user)

        # filter by the staff member
        qs = Task.objects.filter(staff=self.staff)

        # filter for past range
        qs = qs.filter(completed__lte=self.end_date, completed__gt=self.start_date)

        # filter for search term
        if self.search_term != '':
            qs = qs.filter(
                    description__contains=self.search_term)

        # order by day
        qs = qs.order_by('-completed')
        self.queryset = qs
        return qs

    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context['staff'] = self.staff
        context['start_date'] = self.start_date
        context['end_date'] = self.end_date
        context['today'] = datetime.datetime.today()
        context['total_tasks'] = self.queryset.count()
        if self.search_term != '':
            context['search_count'] = self.queryset.count()
            context['search_term'] = self.search_term
        for task in self.queryset:
            print(Location.objects.filter(polygon__contains=task.point))
        return context


class StaffDetail(DetailView):
    model = Staff
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    template_name = 'staff_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StaffDetail, self).get_context_data(**kwargs)
        context['earliest_record'] = Task.objects.filter(staff=self.object).earliest()

        context['years'] = []
        for year in ('2016', '2017'):
            start_date = datetime.datetime.strptime(year + "-01-01", "%Y-%m-%d")
            end_date = datetime.datetime.strptime(year + "-12-31", "%Y-%m-%d")
            # filter by the staff member and date range
            qs = Diary.objects.filter(staff=self.object).filter(
                    day__lte=end_date, day__gt=start_date)
            d = {}
            d['days_worked'] = qs.filter(hours__gt=0.0).count()
            d['total_hours'] = qs.aggregate(total_hours=Sum('hours'))['total_hours']
            d['total_tasks'] = Task.objects.filter(
                    completed__in=qs.values_list('day', flat=True)).count()
            d['year'] = year
            context['years'].append(d)
        return context


class DiaryList(ListView):
    template_name = 'diary_list.html'
    context_object_name = 'diary'
    paginate_by = 30
    end_date = None
    start_date = None
    default_range = 7 # 7 days
    search_term = ''

    def get(self, request, *args, **kwargs):
        """Insert logic here before ``get_queryset`` and ``get_context_data are called.

        Figure out number of days and start date based on user input.

        Default is to make a range of the past 7 days.
        """
        start_date = self.request.GET.get('start-date', None)
        end_date = self.request.GET.get('end-date', None)

        if start_date is not None and end_date is not None:
            self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            self.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        else:
            self.end_date = datetime.datetime.today()
            self.start_date = self.end_date - datetime.timedelta(days=self.default_range)

        self.search_term = self.request.GET.get('q', '')

        return super(DiaryList, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """Collect diary entries for this user.

        Show particular date ranges: past week, past month, past year.

        Also filter by a search term which will highlight tasks containing the search term.
        """
        self.user = get_object_or_404(User, username=self.kwargs.get('username'))
        self.staff = get_object_or_404(Staff, user=self.user)

        # filter by the staff member
        qs = Diary.objects.filter(staff=self.staff)

        # filter for past range
        qs = qs.filter(day__lte=self.end_date, day__gt=self.start_date)

        # order by day
        qs = qs.order_by('-day')
        self.queryset = qs
        return qs

    def get_context_data(self, **kwargs):
        context = super(DiaryList, self).get_context_data(**kwargs)
        context['staff'] = self.staff
        context['start_date'] = self.start_date
        context['end_date'] = self.end_date
        context['today'] = datetime.datetime.today()

        # get some useful summary data about the queryset
        context['days'] = self.queryset.count()
        context['days_worked'] = self.queryset.filter(hours__gt=0.0).count()
        context['total_hours'] = self.queryset.aggregate(total_hours=Sum('hours'))['total_hours']
        task_qs = Task.objects.filter(completed__in=self.queryset.values_list('day', flat=True))
        context['total_tasks'] = task_qs.count()
        if self.search_term != '':
            context['search_count'] = task_qs.filter(
                    description__contains=self.search_term).count()
            context['search_term'] = self.search_term
        # get query string to be included in pagination links
        qd = QueryDict(self.request.GET.urlencode(), mutable=True)
        try:
            qd.pop('page')
        except KeyError:
            pass
        context['query_string'] = '?' + qd.urlencode() + '&' if qd else '?'
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
        /caretaking/diary/2017/Mar/10/1/
        >>> response = client.get(diary.get_absolute_url())
        >>> print(response.status_code)
        200
        >>> print(len(response.context['object'].tasks))
        20
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
        try:
            context['next'] = self.object.get_next_by_day()
        except Diary.DoesNotExist:
            context['next'] = None
        try:
            context['previous'] = self.object.get_previous_by_day()
        except Diary.DoesNotExist:
            context['previous'] = None

        return context
