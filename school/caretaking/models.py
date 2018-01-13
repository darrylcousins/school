__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import random

from django.db import models, connection
from django.urls import reverse
from django.contrib.gis import geos
from django.contrib.gis.db.models.fields import GeometryField
from django.contrib.gis.db.models.functions import Centroid


class Staff(models.Model):
    """
    The member/s of staff assigned to the task in the case of an uncompleted task and the member/s
    of staff whom completed the task.

    Must be a django user of the application.::

        >>> from django.contrib.auth.models import User
        >>> darryl, created = User.objects.get_or_create(username='cousinsd', first_name='Darryl',
        ...     last_name='Cousins')
        >>> if created:
        ...     darryl.save()
        >>> caretaker, created = Staff.objects.get_or_create(user=darryl, title='Caretaker')
        >>> if created:
        ...     caretaker.save()
        >>> print(caretaker)
        Darryl Cousins (Caretaker)

    """
    staffid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)

    def __str__(self):
        "Returns the person's full name."
        return '%s %s (%s)' % (
                self.user.first_name, self.user.last_name, self.title)

    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'


class Location(models.Model):
    """
    Provide a location, a geospatial polygon describing a part of the school::

        >>> library = Location.objects.create(name='Library',
        ...     polygon='POLYGON ((1 1, 3 3, 3 1, 1 1))')
        >>> library.save()
        >>> print(library)
        Library
        >>> print(library.polygon)
        SRID=4326;POLYGON ((1 1, 3 3, 3 1, 1 1))

    Locate the centre of the polygon using ``STCentroid()``.

        >>> print(library.polygon.centroid)
        SRID=4326;POINT (2.333333333333334 1.666666666666667)

    """
    locationid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    polygon = GeometryField()

    def __str__(self):
        "Returns the location's name."
        return self.name

    class Meta:
        ordering = ('name',)


class TaskType(models.Model):
    """
    A type of task, e.g. maintenance, natural repairs, damage repairs, requests and improvemets.::

        >>> maintenance, created = TaskType.objects.get_or_create(name='Maintenance')
        >>> if created:
        ...     maintenance.save()
        >>> print(maintenance)
        Maintenance

    """
    typeid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        "Returns the task type's name."
        return self.name


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
        ...     point='POINT (172.29307 -43.75858)')
        >>> todo.save()
        >>> print(todo)
        Clear downpipe at library

    It can have more than one point of activity::

        >>> todo.point = 'MULTIPOINT ((172.29307 -43.75858), (172.30 -43.76))'
        >>> todo.save()

    Assign the task::

        >>> todo.staff.add(caretaker)
        >>> print([str(s) for s in todo.staff.all()])
        ['Darryl Cousins (Caretaker)']

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
    taskid = models.AutoField(primary_key=True)
    description = models.TextField(blank=False, null=False)
    completed = models.DateField(blank=True, null=True)
    urgency = models.CharField(
            max_length=4,
            choices=URGENCY,
            default='low'
            )
    tasktype = models.ManyToManyField(
        'TaskType',
        blank=True)
    staff = models.ManyToManyField(
        'Staff',
        blank=True)
    point = GeometryField()
    comment = models.TextField(blank=True, null=True)

    class Meta:
        get_latest_by = 'completed'

    def __str__(self):
        "Returns completed date and a truncated line of the tasks description."
        day = self.completed.strftime("%a %d %b %Y") if self.completed else None
        if day:
            return '{0} {1:.100}'.format(day, self.description)
        else:
            return '{:.100}'.format(self.description)

    def locations(self):
        return Location.objects.filter(
            polygon__intersects=self.point).exclude(name='CollegeBoundary')

class Diary(models.Model):
    """
    A day to day record of tasks completed.

    A diary needs a staff member::

        >>> from django.contrib.auth.models import User
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
        >>> diary = Diary.objects.create(day=date(2017, 3, 10), hours=10.5, staff=caretaker, comment=None)
        >>> diary.save()
        >>> print(diary)
        Fri 10 Mar 2017 Darryl Cousins (Caretaker)

    Create a bunch of tasks::

        >>> thispoint = 'MULTIPOINT ((172.29307 -43.75858), (172.30 -43.76))'
        >>> for i in range(10):
        ...     t = Task.objects.create(description=str(i),
        ...         completed=diary.day,
        ...         point=thispoint)
        ...     t.save()
        ...     t.staff.add(caretaker)

    Getting tasks completed on this diary day::

        >>> diary.tasks
        <QuerySet [...]>

    """
    diaryid = models.AutoField(primary_key=True)
    day = models.DateField() # the day of this diary entry
    hours = models.FloatField() # number of hours worked
    staff = models.ForeignKey(
        'Staff',
        on_delete=models.DO_NOTHING)
    comment = models.TextField(blank=True, null=True)

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
        }

    def get_absolute_url(self):
        return reverse('diary-detail', kwargs=self.get_url_kwargs())

    def get_edit_url(self):
        return reverse('diary-edit', kwargs=self.get_url_kwargs())

    @property
    def tasks(self):
        """Return iterable of tasks completed on this day by this staff
        """
        return Task.objects.filter(completed=self.day).filter(staff__in=[self.staff])

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
        
        Where to put this algorithm?
        
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


class Project(models.Model):
    """
    A project. Will be made up of a number of tasks.


    """
    projectid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        'Staff',
        related_name='+', # don't create a backwards set
        on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        'Staff',
        on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    tasks = models.ManyToManyField(
        'Task',
        blank=True)

    def __str__(self):
        "Returns the project's name."
        return self.name


