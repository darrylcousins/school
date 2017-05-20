__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.db import models, connection
from django.contrib.gis.db.models.fields import GeometryField
from django.urls import reverse


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
    user = models.ForeignKey('auth.User')

    @property
    def firstname(self):
        return self.user.first_name

    @property
    def lastname(self):
        return self.user.last_name

    def __str__(self):
        "Returns the person's full name."
        return '%s %s (%s)' % (self.firstname, self.lastname, self.title)

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

        >>> print(library.centroid())
        POINT (2.3333333333333357 1.6666666666666714)

    """
    # TODO constrain polygon to polygon geometry
    locationid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    polygon = GeometryField()

    def centroid(self):
        sql = "select polygon.MakeValid().STCentroid().STAsText() "
        sql += "from caretaking_location "
        sql += "where name = %s"
        with connection.cursor() as cursor:
            result = cursor.execute(sql, [self.name])
            centroid = result.fetchone()
        return centroid[0]

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
        >>> todo.completed = date(2017, 3, 10)
        >>> todo.save()
        >>> print(todo.completed)
        2017-03-10
        >>> print(todo)
        Fri 10 Mar 2017 Clear downpipe at library

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

    def __str__(self):
        "Returns completed date and a truncated line of the tasks description."
        day = self.completed.strftime("%a %d %b %Y") if self.completed else None
        if day:
            return '{0} {1:.100}'.format(day, self.description)
        else:
            return '{:.100}'.format(self.description)

    #def get_absolute_url(self):
    #    return reverse('task-detail', args=[str(self.taskid)])


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

    Getting tasks completed on this diary day::

        >>> diary.tasks
        <QuerySet []>

    """
    diaryid = models.AutoField(primary_key=True)
    day = models.DateField()
    hours = models.FloatField()
    staff = models.ForeignKey(
        'Staff',
        on_delete=models.DO_NOTHING)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        "Returns the day and staff member name."
        return '%s %s' % (self.day.strftime("%a %d %b %Y"), self.staff)

    def get_absolute_url(self):
        return reverse('diary-detail', args=[str(self.diaryid)])

    @property
    def tasks(self):
        return Task.objects.filter(completed=self.day)

    class Meta:
        verbose_name = 'Diary'
        verbose_name_plural = 'Diaries'


