__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import re

from caretaking.models import TaskType


class TypeTask:
    """Class to find points from text description

    Load task type fixtures::

        >>> from django.core.management import call_command
        >>> call_command('loaddata', 'tasktype.json', verbosity=0)
        >>> from caretaking.models import TaskType

        >>> gp = TypeTask('open, heating, etc')
        >>> gp.types()
        [<TaskType: Duties>]
        >>> gp = TypeTask('clear rubbish from canteen concourse')
        >>> gp.types()
        [<TaskType: Duties>]
        >>> gp = TypeTask('remove and repair shelving from')
        >>> gp.types()
        [<TaskType: Duties>]

    """
    types_dict = {
            'Duties': '(^open,)|(^lock up)|(rubbish)|(boiler)',
            'Repairs': '(repair)',
            }

    def __init__(self, text):
        """Initialize with the text to be searching."""
        self.text = text

    def compile(self, pattern):
        """Return case-insensitive search pattern"""
        return re.compile(pattern, flags=re.IGNORECASE)

    def search(self, pattern):
        """Use python regex to search the text"""
        return re.search(self.compile(pattern), self.text)

    def types(self):
        """Get the task types indicated in the text"""
        types = []
        for task_type, pattern in self.types_dict.items():
            match = self.search(pattern)
            if match:
                types.append(TaskType.objects.get(name=task_type))
        return types
