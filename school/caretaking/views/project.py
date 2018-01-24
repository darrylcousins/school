__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.views.generic import ListView
from django.views.generic.edit import CreateView

from caretaking.models import Project
from caretaking.views.mixins import StaffRequiredMixin

### Project views
class ProjectList(StaffRequiredMixin, ListView):
    model = Project
    template_name = 'project_list.html'


class ProjectAdd(StaffRequiredMixin, CreateView):
    model = Project
    template_name = 'project_add_form.html'
    fields = ['name', 'description', 'comment', 'tasks']
