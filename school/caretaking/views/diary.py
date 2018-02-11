__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import datetime
import base64
from io import BytesIO

from django.db.models import Sum
from django.http.request import QueryDict
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.dates import DateDetailView
from django.contrib.auth.models import User
from django.contrib.gis import gdal, geos
from django.forms import modelform_factory
from django.forms import HiddenInput

from wordcloud import WordCloud, STOPWORDS

from caretaking.models import Diary, Staff
from caretaking.models import Location, Task
from caretaking.utils import QueryBuilder
from caretaking.views.mixins import StaffRequiredMixin
from caretaking.views.utils import color_func, FONT_PATH


### Diary views
class DiaryAdd(StaffRequiredMixin, CreateView):
    model = Diary
    template_name = 'diary_add_form.html'
    fields = ['day', 'hours', 'staff', 'comment']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = datetime.datetime.today()
        try:
            latest = Diary.objects.filter(staff=self.staff).latest('day').day
            context['next_day'] = latest + datetime.timedelta(days=1)
        except Diary.DoesNotExist:
            context['next_day'] = context['today']
        context['staff'] = self.staff
        return context

    def get_success_url(self):
        return self.object.get_edit_url()

    def get_initial(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return {
            'staff': user.staff
        }


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
        context['staff'] = self.staff
        return context


class DiaryList(ListView):
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

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """Collect diary entries for this user.

        Show particular date ranges: past week, past month, past year.

        Also filter by a search term which will highlight tasks containing the search term.
        """
        self.user = get_object_or_404(User, username=self.kwargs.get('username'))

        # filter by the staff member
        qs = Diary.objects.filter(staff=self.user.staff)

        # filter for past range
        qs = qs.filter(day__lte=self.end_date, day__gte=self.start_date)

        # order by day
        qs = qs.order_by('-day')
        self.queryset = qs
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff'] = self.user.staff
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
        /caretaking/cousinsd/diary/2017/Mar/10/1/
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
