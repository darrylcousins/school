__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.urls import reverse
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


class ProjectConfirmDelete(StaffRequiredMixin, DeleteView):
    model = Project
    template_name = 'project_confirm_delete.html'

    def get_success_url(self):
        return reverse('project-list')


class ProjectEdit(StaffRequiredMixin, UpdateView):
    model = Project
    template_name = 'project_edit_form.html'
    fields = ['name', 'description', 'created_by', 'assigned_to', 'tasks']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff'] = self.staff
        return context


class ProjectAdd(StaffRequiredMixin, AjaxResponseMixin, CreateView):
    model = Project
    template_name = 'project_add_form.html'
    fields = ['name', 'description', 'created_by', 'assigned_to', 'tasks']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff'] = self.staff
        return context

    def get_initial(self):
        return {
            'created_by': self.request.user.staff,
            'assigned_to': self.request.user.staff
        }

