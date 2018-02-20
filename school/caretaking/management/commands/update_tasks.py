__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.core.management.base import BaseCommand, CommandError

from caretaking.models import Task
from caretaking.models import TaskType

class Command(BaseCommand):
    help = "Update tasks to include security task type"

    requires_migrations_checks = True

    def handle(self, *args, **options):
        """Lazy no error checking, relies on good collection of data.
        
        Uses a list of polygons to generate sql to insert CollegePlan MULTIPOLYGON object.
        """
        security = TaskType.objects.get(name='Security')
        qs = Task.objects.filter(
                completed__year='2018').filter(
                description__contains='lock').exclude(
                description__contains='block')
        for task in qs:
            if not security in task.tasktype.all():
                task.tasktype.add(security)
                task.save()
        return

