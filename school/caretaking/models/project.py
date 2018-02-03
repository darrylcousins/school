__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


class Project(models.Model):
    """
    A project. Will be made up of a number of tasks.


    """
    projectid = models.AutoField(
            primary_key=True)
    name = models.CharField(
            max_length=50,
            help_text=_("A short descriptive name"))
    description = models.TextField(blank=True, null=True,
            help_text=_("Long description"))
    created_by = models.ForeignKey(
            'Staff',
            related_name='+', # don't create a backwards set
            on_delete=models.DO_NOTHING,
            help_text=("The staff member who creates the project"))
    assigned_to = models.ForeignKey(
            'Staff',
            blank=True,
            null=True,
            on_delete=models.CASCADE,
            help_text=_("The staff member to whom the project is assigned"))
    comment = models.TextField(
            blank=True, null=True,
            help_text=_("Any additional comments"))
    tasks = models.ManyToManyField(
            'Task',
            help_text=_("The individual tasks that make up the project"))

    def __str__(self):
        "Returns the project's name."
        return self.name

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})
