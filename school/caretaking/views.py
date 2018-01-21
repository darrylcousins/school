__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import datetime
import random
import base64
import json
from io import BytesIO

from django.db.models import Sum, Count, Q
from django.http import JsonResponse
from django.http.request import QueryDict
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.dates import DateDetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.detail import BaseDetailView
from django.contrib.auth.models import User
from django.contrib.gis import gdal, geos
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.forms import modelform_factory
from django.forms import HiddenInput

from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot
from palettable.colorbrewer import sequential

from caretaking.models import Diary, Staff
from caretaking.models import Location, Task, Project
from caretaking.utils import QueryBuilder
from caretaking.management.locate_task import LocateTask

# path to fonts for wordcloud - TODO move to settings or similar
FONT_PATH = 'C:\Windows\Fonts\Candara.ttf'

### Utils
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """fonts and colours for wordcloud"""
    return tuple(sequential.PuBuGn_9.colors[random.randint(2,8)])

### Mixins
class AjaxDeletionMixin:

    def post(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        pk = self.object.pk
        self.object.delete()
        data = {'pk': pk}
        return JsonResponse(data)


class AjaxResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            response = super().form_invalid(form)
            return response

    def form_valid(self, form):
        """Serialize object to return as json response"""
        self.object = form.save()
        if self.request.is_ajax():
            fields = list(form.cleaned_data.keys())
            if 'pk' not in fields:
                fields.append('pk')
            data = json.loads(serializers.serialize('json', 
                    [self.object],
                    fields=fields))[0]
            if getattr(self, 'get_edit_url', False):
                data['edit-url'] = self.get_edit_url()
            if getattr(self, 'get_delete_url', False):
                data['delete-url'] = self.get_delete_url()
            return JsonResponse(data)
        else:
            response = super().form_valid(form)
            return response


class StaffRequiredMixin(LoginRequiredMixin):
    """Mixin to provide staff user for view. TODO raise Unauthenticated or similar.
    """

    def get_context_data(self, **kwargs):
        context = super(LoginRequiredMixin, self).get_context_data(**kwargs)
        self.user = self.request.user
        self.staff = get_object_or_404(Staff, user=self.user)
        print('StaffRequiredMixin', self.staff, self.staff.user)
        context['staff'] = self.staff
        return context


### Staff views
class StaffList(StaffRequiredMixin, ListView):
    model = Staff
    template_name = 'staff_list.html'


class StaffDetail(StaffRequiredMixin, DetailView):
    """
        >>> staff = Staff.objects.first()

    Set up test client::

        >>> from django.test import Client
        >>> client = Client()

    Get url::

        >>> from django.urls import reverse
        >>> url = reverse('staff-detail', kwargs={'username':staff.user.username})
        >>> response = client.get(url)
        >>> print(response.status_code)
        200
        >>> print(response.context['object'])
        Darryl Cousins (Caretaker)

    """
    model = Staff
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    template_name = 'staff_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StaffDetail, self).get_context_data(**kwargs)
        try:
            context['earliest_record'] = Task.objects.filter(staff=self.object).earliest()
        except Task.DoesNotExist:
            pass

        context['years'] = []
        for year in ('2016', '2017', '2018'):
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


### Project views
class ProjectList(StaffRequiredMixin, ListView):
    model = Project
    template_name = 'project_list.html'


class ProjectAdd(StaffRequiredMixin, CreateView):
    model = Project
    template_name = 'project_add_form.html'
    fields = ['name', 'description', 'comment', 'tasks']


### Task views
class TaskAdd(StaffRequiredMixin, AjaxResponseMixin, CreateView):
    model = Task
    template_name = 'task_add_form.html'
    fields = ['completed', 'urgency', 'staff', 'description', 'tasktype']

    def get_context_data(self, **kwargs):
        context = super(TaskAdd, self).get_context_data(**kwargs)
        context['today'] = datetime.datetime.today()
        return context

    def form_valid(self, form):
        description = form.cleaned_data['description']
        form.instance.point = LocateTask(description).points()
        return super().form_valid(form)

    def get_edit_url(self):
        """Provide edit url to be passed back to 'diary-edit' page"""
        return reverse('task-edit',
                kwargs={'username': self.object.staff.user.username,
                    'pk': self.object.pk})

    def get_delete_url(self):
        """Provide delete url to be passed back to 'diary-edit' page"""
        return reverse('task-delete',
                kwargs={'username': self.object.staff.user.username,
                    'pk': self.object.pk})


class TaskEdit(StaffRequiredMixin, UpdateView):
    model = Task
    template_name = 'task_edit_form.html'
    fields = ['completed', 'urgency', 'staff', 'description', 'tasktype']


class TaskEditAjax(StaffRequiredMixin, AjaxResponseMixin, UpdateView):
    model = Task
    template_name = 'task_edit_form.html'
    fields = ['completed', 'urgency', 'staff', 'description']


class TaskDelete(StaffRequiredMixin, BaseDetailView, AjaxDeletionMixin):
    model = Task


class TaskList(ListView):
    model = Task
    template_name = 'task_list.html'
    paginate_by = 30
    end_date = None
    start_date = None
    default_range = 7 # 7 days
    search_phrase = ''
    qb = None

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

        self.search_phrase = self.request.GET.get('q', '')
        locations = self.request.GET.getlist('loc', [])
        self.locations = Location.objects.filter(pk__in=locations)

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

        # filter by selected locations using constructed OR query
        if self.locations:
            queries = [Q(point__intersects=loc.polygon) for loc in self.locations]
            query = queries.pop()
            for q in queries:
                query |= q
            qs = Task.objects.filter(query)

        # filter for past range
        qs = qs.filter(completed__lte=self.end_date, completed__gt=self.start_date)

        # filter for search term
        if self.search_phrase != '':
            self.qb = QueryBuilder(self.search_phrase, 'description')
            self.qb.parse_parts()
            #qs = qs.filter(
            #        description__contains=self.search_phrase)
            qs = qs.filter(self.qb.query)

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
        if self.search_phrase != '':
            context['search_count'] = self.queryset.count()
            context['search_phrase'] = self.search_phrase
            context['search_words'] = ' '.join(self.qb.words)
        # exclude CollegePlan and CollegeBoundary
        context['locations'] = Location.objects.exclude(name__startswith='College')
        context['selected_locations'] = self.locations
        context['selected_location_pks'] = self.locations.values_list('pk', flat=True)
        return context


### Diary views
class DiaryAdd(StaffRequiredMixin, CreateView):
    model = Diary
    template_name = 'diary_add_form.html'
    fields = ['day', 'hours', 'staff', 'comment']

    def get_context_data(self, **kwargs):
        context = super(DiaryAdd, self).get_context_data(**kwargs)
        context['today'] = datetime.datetime.today()
        latest = Diary.objects.filter(staff=self.staff).latest('day').day
        context['next_day'] = latest + datetime.timedelta(days=1)
        return context

    def get_success_url(self):
        return self.object.get_edit_url()


class DiaryEdit(StaffRequiredMixin, UpdateView):
    model = Diary
    template_name = 'diary_edit_form.html'
    fields = ['day', 'hours', 'staff', 'comment']

    def get_context_data(self, **kwargs):
        context = super(DiaryEdit, self).get_context_data(**kwargs)
        context['task_add_form'] = modelform_factory(Task,
            fields=['description', 'tasktype', 'staff', 'urgency', 'completed'],
            widgets={'staff': HiddenInput(),
                'urgency': HiddenInput(),
                'completed': HiddenInput()})
        return context


class DiaryList(StaffRequiredMixin, ListView):
    template_name = 'diary_list.html'
    context_object_name = 'diary'
    paginate_by = 30
    end_date = None
    start_date = None
    default_range = 7 # 7 days
    search_phrase = ''

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

        self.search_phrase = self.request.GET.get('q', '')

        return super(DiaryList, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """Collect diary entries for this user.

        Show particular date ranges: past week, past month, past year.

        Also filter by a search term which will highlight tasks containing the search term.
        """
        self.user = get_object_or_404(User, username=self.kwargs.get('username'))
        self.member = get_object_or_404(Staff, user=self.user)

        # filter by the staff member
        qs = Diary.objects.filter(staff=self.member)

        # filter for past range
        qs = qs.filter(day__lte=self.end_date, day__gt=self.start_date)

        # order by day
        qs = qs.order_by('-day')
        self.queryset = qs
        return qs

    def get_context_data(self, **kwargs):
        context = super(DiaryList, self).get_context_data(**kwargs)
        context['member'] = self.member
        context['start_date'] = self.start_date
        context['end_date'] = self.end_date
        context['today'] = datetime.datetime.today()

        # get some useful summary data about the queryset
        context['days'] = self.queryset.count()
        context['days_worked'] = self.queryset.filter(hours__gt=0.0).count()
        context['total_hours'] = self.queryset.aggregate(total_hours=Sum('hours'))['total_hours']
        task_qs = Task.objects.filter(completed__in=self.queryset.values_list('day', flat=True))
        context['total_tasks'] = task_qs.count()

        # filter for search term
        if self.search_phrase != '':
            qb = QueryBuilder(self.search_phrase, 'description')
            qb.parse_parts()
            context['search_count'] = task_qs.filter(qb.query).count()
            context['search_phrase'] = self.search_phrase
            context['search_words'] = ' '.join(qb.words)

        # create word cloud from task descriptions
        words = ' '.join(task_qs.values_list('description', flat=True)).lower()
        if words:
            stopwords = set(STOPWORDS)
            stopwords.add('block')

            cloud = WordCloud(background_color='white', stopwords=stopwords,
                    width=960, height=100, max_font_size=50, min_font_size=2,
                    font_path=FONT_PATH, max_words=300, prefer_horizontal=0.8)
            cloud.generate(words)
            cloud.recolor(color_func=color_func, random_state=3)
            img = cloud.to_image()

            in_mem_file = BytesIO()
            img.save(in_mem_file, format="PNG")
            img_bytes = in_mem_file.getvalue()
            result_bytes = base64.b64encode(img_bytes)
            result_str = result_bytes.decode('ascii')
            context['wordcloud'] = 'data:image/png;base64,' + result_str

        # query string to be included in pagination links
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
        ...         point=thispoint,
        ...         staff=task.staff)
        ...     t.save()

    Set up test client::

        >>> from django.test import Client
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
    allow_future = True

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


class DiaryDelete(StaffRequiredMixin, DeleteView):
    model = Diary
    template_name = 'diary_confirm_delete.html'

    def get_success_url(self):
        return reverse('diary-list', kwargs={'username': self.request.user.username})
