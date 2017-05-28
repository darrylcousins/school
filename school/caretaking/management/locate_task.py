__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import re

from django.contrib.gis import gdal, geos

from caretaking.models import Location


class LocateTask:
    """Class to find points from text description

    Load location fixtures::

        >>> from django.core.management import call_command
        >>> call_command('loaddata', 'location', verbosity=0)
        >>> from caretaking.models import Location

    If no match is found the default college centroid is returned::

        >>> gp = LocateTask('change bulb')
        >>> assert gp.points() == gp.college

    If a single match is found the WKT representation of a point is returned::

        >>> gp = LocateTask('change bulb in A block')
        >>> assert gp.points() == Location.objects.get(name='ABlock').centroid()

    If multiple matches are found the WKT representation of a multipoint is returned::

        >>> gp = LocateTask('change bulb in A and B block')
        >>> print(gp.points())
        MULTIPOINT ...

    """
    # centre point of school building extent - used if no other location point defined
    college = 'POINT (172.292576 -43.757829)'
    srid = 3587
    location_dict = {
            'ABlock': 'a( |-)(and b )?block',
            'BBlock': 'b( |-)block',
            'CBlock': 'c( |-)block',
            'HBlock': 'h( |-)block',
            'OBlock': 'o( |-)block',
            'PBlock': 'p( |-)block',
            'HomeEconomics': 'home ec',
            'Textile': 'textile',
            'Art': 'art',
            'Administration': 'admin|sick bay',
            'Hall': 'gym|hall',
            'Stage': 'stage',
            'WilsonRoom': 'wilson r(oo)?m',
            'Design': 'kelly r(oo)?m',
            'GymChangingRoom': 'changing r(oo)?m',
            'Library': 'library',
            'Music': 'music',
            'ServerRoom': 'server room',
            'ScienceTech': 'sci(ence)?\.? tech',
            'HBlockNorth': '(r(oo)?ms?)? 12/13',
            'HBlockSouth': '(r(oo)?ms?)? 14/15',
            'Room1': 'r(oo)?m 1( |$)',
            'Room2': 'r(oo)?m 2( |$)',
            'Room3': 'r(oo)?m 3( |$)',
            'Room4': 'r(oo)?m 4( |$)',
            'Room5': 'r(oo)?m 5( |$)',
            'Room6': 'r(oo)?m 6( |$)',
            'Room7': 'r(oo)?m 7( |$)',
            'Room9': 'r(oo)?m 9( |$)',
            'Room10': 'r(oo)?m 10( |$)',
            'Room12': 'r(oo)?m 12( |$)',
            'Room13': 'r(oo)?m 13( |$)',
            'Room14': 'r(oo)?m 14( |$)',
            'Room15': 'r(oo)?m 15( |$)',
            'Room16': 'r(oo)?m 16( |$)',
            'SCR': 'scr',
            'Math': '(r(oo)?ms?)? 17/18',
            'Room17': 'r(oo)?m 17( |$)',
            'Room18': 'r(oo)?m 18( |$)',
            'English': '(r(oo)?ms?)? 19/20',
            'Room19': 'r(oo)?m 19( |$)',
            'Room20': 'r(oo)?m 20( |$)',
            'Room21': 'r(oo)?m 21( |$)',
            'Room22': 'r(oo)?m 22( |$)',
            'Room23': 'r(oo)?m 23|careers?',
            'Room24': 'r(oo)?m 24|jap(anese)?',
            'LabA': 'lab a',
            'LabB': 'lab b',
            'LabC': 'lab c',
            'LabP': 'lab p',
            'Canteen': 'canteen',
            'Woodshop': 'wood(shop|work)',
            'Metalshop': 'metal(shop|work)',
            'VanGarage': 'van garage',
            'TractorShed': 'tractor shed|garage',
            'Boiler': 'boiler',
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
        value = None
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



