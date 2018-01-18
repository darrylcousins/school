import csv
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from caretaking.models import Staff, Diary, Task, TaskType, Location
from caretaking.management.locate_task import LocateTask
from caretaking.management.type_task import TypeTask

class Command(BaseCommand):
    """
    Regex expressions to locate tasks.

        >>> from django.core.management import call_command
        >>> # TODO create and use a test csv file (to avoid the 11000 rows here)
        >>> # call_command('importdiary')

    """
    help = "Imports tab delimited csv files as exported from google spreadsheet data"
    help += "Use with caution - will first delete all current records"
    requires_migrations_checks = True

    def handle(self, *args, **options):
        """Lazy no error checking, relies on good collection of data.
        """

        # create staff member for this set of tasks
        darryl, created = User.objects.get_or_create(username='cousinsd', first_name='Darryl',
            last_name='Cousins')
        darryl.is_staff = True
        darryl.is_superuser = True
        darryl.set_password('car3tak3')
        if created:
            darryl.save()

        caretaker, created = Staff.objects.get_or_create(user=darryl, title='Caretaker')
        if created:
            caretaker.save()

        # create task types from fixtures/tasktype.json
        call_command('loaddata', 'tasktype.json', verbosity=0)

        # delete all rows
        sql ="DELETE FROM caretaking_%s;"
        pksql = "DBCC CHECKIDENT(caretaking_%s, RESEED, 0);"
        with connection.cursor() as cursor:
            cursor.execute(sql % 'task_staff')
            cursor.execute(sql % 'task_tasktype')
            cursor.execute(sql % 'task')
            cursor.execute(sql % 'diary')
            cursor.execute(sql % 'task')
            #cursor.execute(pksql % 'task_staff')
            #cursor.execute(pksql % 'task_tasktype')
            #cursor.execute(pksql % 'task')
            #cursor.execute(pksql % 'diary')
            #cursor.execute(pksql % 'task')

        # older data has different column format
        reader = csv.reader(open('caretaking/data/jan_oct.csv'), delimiter='\t')
        for row in reader:
            day = row[0]
            day = datetime.strptime(day, '%a %d %b %Y').date()
            try:
                hours = float(row[9])
            except:
                hours = 0.0
            comment = row[15]
            diary, created = Diary.objects.get_or_create(day=day, hours=hours, staff=caretaker, comment=comment)
            if created:
                diary.save()
            tasklist = []
            for idx in (2, 4, 6, 8):
                tasklist += [s.strip() for s in row[idx].split('*')]
            tasklist = [t for t in tasklist if t]
            for t in tasklist:
                # use regex to identify if possible a point
                point = LocateTask(t).points()
                task = Task.objects.create(description=t, urgency='high',
                    point=point, completed=day, staff=caretaker)
                task.save()

        # and the newer data
        reader = csv.reader(open('caretaking/data/oct_current.csv'), delimiter='\t')
        count = 0
        for row in reader:
            day = row[0]
            day = datetime.strptime(day, '%a %d %b %Y').date()
            try:
                hours = float(row[1])
            except:
                hours = 0.0
            try:
                comment = row[4]
            except IndexError:
                comment = ''
            diary, created = Diary.objects.get_or_create(day=day, hours=hours, staff=caretaker, comment=comment)
            if created:
                diary.save()
            count += 1
            tasklist = [s.strip() for s in row[2].split('*')]
            tasklist = [t for t in tasklist if t]
            for t in tasklist:
                point = LocateTask(t).points()
                task = Task.objects.create(description=t, urgency='high',
                    point=point, completed=day, staff=caretaker)
                task.save()
                for task_type in TypeTask(t).types():
                    task.tasktype.add(task_type)

