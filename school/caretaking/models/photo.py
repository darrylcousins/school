__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.apps import apps
from django.utils.translation import gettext as _


class Photo(models.Model):
    """
    A photo which I hope to connect to any model object that is chosen

        >>> from caretaking.models import Task
        >>> task = Task.objects.first()

    Get the primary key of the Task::

        >>> model = 'caretaking.Task'
        >>> args = model.split('.')

    This string can be used to get to the model and therefore the object::

        >>> from django.apps import apps
        >>> apps.get_model(*args).objects.get(pk=task.pk) == task
        True

    """
    photoid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50,
            help_text=_("Useful title for this photo"))
    description = models.TextField(blank=True, null=True,
            help_text=_("Long description"))
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    model = models.CharField(max_length=50,
            help_text=_("Model that this photo is attached to, e.g. 'caretaking.Task'"))
    model_pk = models.IntegerField(
            help_text=_("The primary key for the particular object of the model"))
    created_by = models.ForeignKey(
            'Staff',
            on_delete=models.DO_NOTHING,
            help_text=("The staff member who uploaded the photo"))

    def __str__(self):
        "Returns the photo's title."
        return self.title

    def get_image_url(self):
        return settings.MEDIA_URL + str(self.image)

    def get_detail_url(self):
        return reverse('photo-detail', kwargs={'pk': self.pk})

    def get_object(self):
        args = self.model.split('.')
        obj = apps.get_model(*args).objects.get(pk=self.model_pk)
        return obj

    def get_absolute_url(self):
        return self.get_object().get_absolute_url()
