__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import random

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.gis import geos
from django.contrib.gis.db.models.fields import GeometryField
from django.contrib.gis.db.models.functions import Centroid

from caretaking.models import Task
from .mixins import PhotoEnabled

class Diary(PhotoEnabled, models.Model):
    """
    A day to day record of tasks completed.

    A diary needs a staff member::

        >>> from django.contrib.auth.models import User
        >>> from caretaking.models import Staff
        >>> darryl, created = User.objects.get_or_create(username='cousinsd', first_name='Darryl',
        ...     last_name='Cousins')
        >>> if created:
        ...     darryl.save()
        >>> caretaker, created = Staff.objects.get_or_create(user=darryl, title='Caretaker')
        >>> if created:
        ...     caretaker.save()

    Using the date field we can list all the tasks performed by the staff member that day. It is my
    expectation that the staff member will provide his or her comments about the day.::

        >>> from datetime import date
        >>> from caretaking.models import Diary
        >>> diary = Diary.objects.create(day=date(2017, 3, 10), hours=10.5, staff=caretaker, comment=None)
        >>> diary.save()
        >>> print(diary)
        Fri 10 Mar 2017 Darryl Cousins (Caretaker)

    Create a bunch of tasks::

        >>> thispoint = 'MULTIPOINT ((172.29307 -43.75858), (172.30 -43.76))'
        >>> for i in range(10):
        ...     t = Task.objects.create(description=str(i),
        ...         completed=diary.day,
        ...         point=thispoint,
        ...         staff=caretaker)
        ...     t.save()

    Getting tasks completed on this diary day::

        >>> diary.tasks
        <QuerySet [...]>

    """
    diaryid = models.AutoField(
            primary_key=True)
    day = models.DateField(
            help_text=_("The date of this diary entry"))
    hours = models.FloatField(
            help_text=_("The hours worked this day"))
    staff = models.ForeignKey(
            'Staff',
            on_delete=models.DO_NOTHING,
            help_text=_("The staff member of this diary entry"))
    comment = models.TextField(blank=True, null=True,
            help_text=_("A summary comment about this day"))

    class Meta:
        verbose_name = 'Diary'
        verbose_name_plural = 'Diaries'
        unique_together = ('day', 'staff') # one diary entry per staff member

    def __str__(self):
        "Returns the day and staff member name."
        return '%s %s' % (self.day.strftime("%a %d %b %Y"), self.staff)

    def get_url_kwargs(self):
        return {
            'pk': str(self.diaryid),
            'year': self.day.strftime('%Y'),
            'month': self.day.strftime('%b'),
            'day': self.day.strftime('%d'),
            'username': self.staff.user.username,
        }

    def get_absolute_url(self):
        return reverse('diary-detail', kwargs=self.get_url_kwargs())

    def get_edit_url(self):
        return reverse('diary-edit', kwargs=self.get_url_kwargs())

    def get_delete_url(self):
        return reverse('diary-delete', kwargs=self.get_url_kwargs())

    def get_confirm_delete_url(self):
        return reverse('diary-confirm-delete', kwargs=self.get_url_kwargs())

    @property
    def tasks(self):
        """Return iterable of tasks completed on this day by this staff
        """
        return Task.objects.filter(completed=self.day).filter(
            staff__in=[self.staff]).order_by('pk')

    def points(self, spread=True):
        """Return iterable of points of work on this day using points from tasks

        spread:
            If true then eliminate duplicates by creating clusters

        # TODO group into task type collections
        """
        point_collection = []
        for task in self.tasks:
            if isinstance(task.point, geos.MultiPoint):
                for point in task.point:
                    point_collection.append(point)
            elif isinstance(task.point, geos.Point):
                point_collection.append(task.point)
        if spread:
            return self.spread(point_collection)
        return point_collection

    def spread(self, point_collection):
        """Take an iterable of points and eliminate duplicates by creating clusters.
        """
        #targets = (0, 1, 2, -1, -2)
        targets = (0, 2, -2)
        targets = [t*0.00001 for t in targets]
        points = []
        for p in point_collection:
            point = p.clone()
            while p in points:
                # change point
                p.x += targets[random.randrange(len(targets))]
                p.y += targets[random.randrange(len(targets))]
                #p.x = round(p.x, 6)
                #p.y = round(p.y, 6)
                if p in points:
                    continue
                else:
                    points.append(p)
                    break
            else:
                points.append(p)
        return points                
