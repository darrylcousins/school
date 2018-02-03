__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.detail import BaseDetailView

from caretaking.models import Project
from caretaking.views.mixins import StaffRequiredMixin
from caretaking.views.mixins import AjaxResponseMixin
from caretaking.views.mixins import AjaxDeletionMixin


### Project views
class ProjectList(ListView):
    model = Project
    template_name = 'project_list.html'


class ProjectDetail(DetailView):
    model = Project
    template_name = 'project_detail.html'


class ProjectDelete(StaffRequiredMixin, BaseDetailView, AjaxDeletionMixin):
    model = Project


class ProjectEdit(UpdateView):
    model = Project
    template_name = 'project_edit.html'
    fields = ['name', 'description', 'created_by', 'assigned_to', 'tasks']


class ProjectAdd(AjaxResponseMixin, CreateView):
    model = Project
    template_name = 'project_add_form.html'
    fields = ['name', 'description', 'created_by', 'assigned_to', 'tasks']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO authorisation test!!!
        context['staff'] = self.request.user.staff
        return context

    def get_initial(self):
        return {
            'created_by': self.request.user.staff,
            'assigned_to': self.request.user.staff
        }

