import csv
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from caretaking.models import Staff, Diary, Task, Location
from caretaking.management.re_locate import ReLocate

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

        # delete all rows
        sql ="DELETE FROM caretaking_%s;"
        with connection.cursor() as cursor:
            cursor.execute(sql % 'task_staff')
            cursor.execute(sql % 'task')
            cursor.execute(sql % 'diary')
            cursor.execute(sql % 'task')

        # older data has different column format
        reader = csv.reader(open('caretaking/data/jan_oct.csv'), delimiter='\t')
        for row in reader:
            day = row[0][4:]
            day = datetime.strptime(day, '%d %b %Y').date()
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
                point = ReLocate(t).get_points()
                task = Task.objects.create(description=t, urgency='high',
                    point=point, completed=day)
                task.save()
                task.staff.add(caretaker)

        # and the newer data
        reader = csv.reader(open('caretaking/data/oct_current.csv'), delimiter='\t')
        for row in reader:
            day = row[0][4:]
            day = datetime.strptime(day, '%d %b %Y').date()
            try:
                hours = float(row[1])
            except:
                hours = 0.0
            try:
                comment = row[4]
            except IndexError:
                print(row)
                comment = ''
            diary, created = Diary.objects.get_or_create(day=day, hours=hours, staff=caretaker, comment=comment)
            if created:
                diary.save()
            tasklist = [s.strip() for s in row[2].split('*')]
            tasklist = [t for t in tasklist if t]
            for t in tasklist:
                point = ReLocate(t).get_points()
                task = Task.objects.create(description=t, urgency='high',
                    point=point, completed=day)
                task.save()
                task.staff.add(caretaker)

