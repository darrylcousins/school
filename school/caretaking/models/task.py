__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.gis.db.models.fields import GeometryField

from caretaking.models.location import Location


class TaskType(models.Model):
    """
    A type of task, e.g. maintenance, natural repairs, damage repairs, requests and improvemets.::

        >>> maintenance, created = TaskType.objects.get_or_create(name='Maintenance')
        >>> if created:
        ...     maintenance.save()
        >>> print(maintenance)
        Maintenance

    """
    typeid = models.AutoField(
            primary_key=True)
    name = models.CharField(
            max_length=50,
            help_text=_("A short descriptive name"))
    comment = models.TextField(
            blank=True, null=True,
            help_text=_("Additional descriptive comment"))

    def __str__(self):
        """Returns the task type's name."""
        return self.name

    class Meta:
        verbose_name = "Task Type"

class Task(models.Model):
    """
    A task, also used to generate a todo list, i.e. those without a completed date.

    Tasks need a staff member/s to do the work::

        >>> from django.contrib.auth.models import User
        >>> darryl, created = User.objects.get_or_create(username='cousinsd', first_name='Darryl',
        ...     last_name='Cousins')
        >>> if created:
        ...     darryl.save()
        >>> caretaker, created = Staff.objects.get_or_create(user=darryl, title='Caretaker')

    A type of task is also required::

        >>> maintenance, created = TaskType.objects.get_or_create(name='Maintenance')
        >>> if created:
        ...     maintenance.save()

    Without a completed date then the task can be considered a todo::

        >>> todo = Task.objects.create(description="Clear downpipe at library", urgency='high',
        ...     point='POINT (172.29307 -43.75858)', staff=caretaker)
        >>> todo.save()
        >>> print(todo)
        Clear downpipe at library
        >>> todo.tasktype.add(maintenance)

    It can have more than one point of activity::

        >>> todo.point = 'MULTIPOINT ((172.29307 -43.75858), (172.30 -43.76))'
        >>> todo.save()

    Assign the task::

        >>> print(todo.staff)
        Darryl Cousins (Caretaker)

    It has a location::

        >>> print(todo.point)
        SRID=4326;MULTIPOINT (172.29307 -43.75858, 172.3 -43.76)

    Maybe the job got done too::

        >>> from datetime import date
        >>> todo.completed = date(2017, 3, 17)
        >>> todo.save()
        >>> print(todo.completed)
        2017-03-17
        >>> print(todo)
        Fri 17 Mar 2017 Clear downpipe at library

    To select tasks for the caretaker::

        >>> Task.objects.filter(staff=caretaker).count()
        11
    
    Accordingly we expect none from the assistant::

        >>> maria, created = User.objects.get_or_create(username='halloumism', first_name='Maria',
        ...     last_name='Halloumis')
        >>> if created:
        ...     maria.save()
        >>> assistant, created = Staff.objects.get_or_create(user=maria, title='Assistant')
        >>> Task.objects.filter(staff=assistant).count()
        0

    We can select earliest and latest Tasks by completed date::

        >>> Task.objects.filter(staff=caretaker).earliest()
        <Task: Fri 10 Mar ...>

    Or a count of tasks completed for the year::

        >>> Task.objects.filter(staff=caretaker).filter(completed__year=2017).count()
        11

    """
    URGENCY = (
            ('low', 'Low'),
            ('med', 'Medium'),
            ('high', 'High')
            )
    taskid = models.AutoField(
            primary_key=True)
    description = models.TextField(
            blank=False, null=False,
            help_text=_("A descriptive summary of the task"))
    completed = models.DateField(
            blank=True, null=True,
            help_text=_("The date completed"))
    urgency = models.CharField(
            max_length=4,
            choices=URGENCY,
            default='low',
            help_text=_("The urgency of the task"))
    tasktype = models.ManyToManyField(
            'TaskType',
            help_text=_("One or more types"))
    staff = models.ForeignKey(
            'Staff',
            blank=True,
            null=True,
            on_delete=models.DO_NOTHING,
            help_text=("Staff member performing the work"))
    point = GeometryField(
            blank=True, null=True,
            help_text=("Point or Multipoint for the task"))

    class Meta:
        get_latest_by = 'completed'
        ordering = ('completed',)

    def __str__(self):
        "Returns completed date and a truncated line of the tasks description."
        day = self.completed.strftime("%a %d %b %Y") if self.completed else None
        if day:
            return '{0} {1:.100}'.format(day, self.description)
        else:
            return '{:.100}'.format(self.description)

    def get_absolute_url(self):
        return reverse('task-list', kwargs={'username': self.staff.user.username})

    def get_diary_url(self):
        from caretaking.models.diary import Diary
        diary = Diary.objects.get(day=self.completed)
        return diary.get_absolute_url()

    def locations(self):
        """Find the location or locations in which the point falls"""
        return Location.objects.filter(
            polygon__intersects=self.point).exclude(name='CollegeBoundary')
