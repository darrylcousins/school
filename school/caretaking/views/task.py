__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import datetime

from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import BaseDetailView

from caretaking.models import Staff
from caretaking.models import Location, Task
from caretaking.utils import QueryBuilder
from caretaking.management.locate_task import LocateTask
from caretaking.views.mixins import AjaxResponseMixin
from caretaking.views.mixins import AjaxDeletionMixin
from caretaking.views.mixins import StaffRequiredMixin
from caretaking.utils import QueryBuilder

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
        context = super().get_context_data(**kwargs)
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
