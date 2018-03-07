__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.urls import reverse
from django.apps import apps
from django.http import Http404
from django.http.request import QueryDict
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.detail import BaseDetailView

from caretaking.models import Photo
from caretaking.views.mixins import StaffRequiredMixin
from caretaking.views.mixins import AjaxResponseMixin
from caretaking.views.mixins import AjaxDeletionMixin


### Photo views
class PhotoList(ListView):
    model = Photo
    template_name = 'photo_list.html'


class PhotoDetail(DetailView):
    model = Photo
    template_name = 'photo_detail.html'


class PhotoUpload(TemplateView):
    template_name = 'photo_upload.html'


class PhotoDelete(StaffRequiredMixin, BaseDetailView, AjaxDeletionMixin):
    model = Photo


class PhotoConfirmDelete(StaffRequiredMixin, DeleteView):
    model = Photo
    template_name = 'photo_confirm_delete.html'

    def get_success_url(self):
        return reverse('photo-list')


class PhotoAdd(StaffRequiredMixin, AjaxResponseMixin, CreateView):
    model = Photo
    template_name = 'photo_add_form.html'
    fields = ['title', 'image', 'description', 'created_by', 'model', 'model_pk']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        args = self.request.GET.get('model').split('.')
        pk = self.request.GET.get('model_pk')
        context['object'] = apps.get_model(*args).objects.get(pk=pk)
        context['staff'] = self.staff
        return context

    def get_initial(self):
        initial = {
            'created_by': self.request.user.staff
        }
        qd = QueryDict(self.request.GET.urlencode())
        if qd:
            initial.update(qd.dict())
        else:
            # not model nor model.pk then raise 404
            raise Http404
        return initial

