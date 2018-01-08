__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import re
from django import template

register = template.Library()

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')
number_re = re.compile('([A-Za-z])([0-9])')

@register.filter(name='convert_camel_case')
def convert_camel_case(name):
    """
    Convert camel case names of Locations::

        >>> s = 'ABlock'
        >>> convert_camel_case(s)
        'A Block'
        >>> s = 'Room12'
        >>> convert_camel_case(s)
        'Room 12'
        >>> s = 'GymChangingRooms'
        >>> convert_camel_case(s)
        'Gym Changing Rooms'

    """
    s1 = first_cap_re.sub(r'\1 \2', name)
    s2 = all_cap_re.sub(r'\1 \2', s1)
    s3 = number_re.sub(r'\1 \2', s2)
    return s3
