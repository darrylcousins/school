__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import re

from caretaking.models import Location


class LocateTask:
    """Class to find points from text description

    Load location fixtures::

        >>> from django.core.management import call_command
        >>> call_command('loaddata', 'location', verbosity=0)
        >>> from caretaking.models import Location

    If no match is found the default college centroid is returned::

        >>> gp = LocateTask('change bulb')
        >>> assert(gp.points() == gp.college)

    If a single match is found the WKT representation of a point is returned::

        >>> gp = LocateTask('change bulb in A block')
        >>> assert(gp.points() == Location.objects.get(name='ABlock').centroid())

    If multiple matches are found the WKT representation of a multipoint is returned::

        >>> gp = LocateTask('change bulb in A and B block')
        >>> print(gp.points())
        MULTIPOINT ...

    """
    # centre point of school building extent - used if no other location point defined
    college = 'POINT (172.292576 -43.757829)'
    location_dict = {
            'ABlock': 'a (and b )?block',
            'BBlock': 'b block',
            'Hall': 'gym|hall',
            'CBlock': 'c block',
            'HBlock': 'h block',
            'Math': 'r(oo)?ms? 17/18',
            'English': 'r(oo)?ms? 19/20',
            'Woodshop': 'wood(shop|work)',
            'Metalshop': 'metal(shop|work)',
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

    def points(self):
        """Get the centroid of the locations indicated in the text"""
        points = []
        for loc, pattern in self.location_dict.items():
            match = self.search(pattern)
            if match:
                points.append(Location.objects.get(name=loc).centroid())
        count = len(points)
        if count == 0:
            # no matches, return college centroid
            return self.college
        elif count == 1:
            # one match, return point only
            return points[0]
        else:
            # multiple matches, combine points into a WKT multipoint representation
            wkt = 'MULTIPOINT (%s)'
            return wkt % ', '.join([p[p.index('('):p.index(')')+1] for p in points])


