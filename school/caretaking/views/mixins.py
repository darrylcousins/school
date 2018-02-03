__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import json

from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core import serializers

from caretaking.models import Staff

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

            # here specifically for Task ajax views
            if getattr(self, 'get_edit_url', False):
                data['edit-url'] = self.get_edit_url()
            if getattr(self, 'get_delete_url', False):
                data['delete-url'] = self.get_delete_url()

            return JsonResponse(data)
        else:
            response = super().form_valid(form)
            return response


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure staff user for view.
    """

    def test_func(self):
        """Authenticated user **must** have a staff object
        
        For all edit views the authenticated user must be the staff member being edited or also
        allow administrators. 
        """
        user = get_object_or_404(User, username=self.kwargs.get('username'))

        self.staff = user.staff

        return bool(user.staff == self.request.user.staff) or self.request.user.is_staff
