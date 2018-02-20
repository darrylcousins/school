__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import datetime

from django.db.models import Sum
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from caretaking.models import Project
from caretaking.models import Staff
from caretaking.models import Diary
from caretaking.models import Staff
from caretaking.models import Task


### Staff views
class StaffList(ListView):
    model = Staff
    template_name = 'staff_list.html'


class StaffDetail(DetailView):
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
        302

    Redirected to login.

    """
    model = Staff
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    template_name = 'staff_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
            d['total_tasks'] = Task.objects.filter(staff=self.object).filter(
                    completed__in=qs.values_list('day', flat=True)).count()
            d['year'] = year
            context['years'].append(d)
        return context
