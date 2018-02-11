__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.core.management.base import BaseCommand, CommandError

from caretaking.models import Location
from caretaking.admin import get_wkt

SQL = """
DELETE FROM caretaking_location WHERE locationid=88;
INSERT INTO caretaking_location(locationid, name, polygon) VALUES(88, 'CollegePlan', ST_GeomFromText('MULTIPOLYGON(%s)', 4326));
"""

class Command(BaseCommand):
    help = "Creates sql. Gather map polygons into single MULTIPOLYGON"
    help += " representing full school plan.\n\n"
    help += "Usage: django manage.py mkcollege > caretaking/sql/college.sql"

    requires_migrations_checks = True

    def handle(self, *args, **options):
        """Lazy no error checking, relies on good collection of data.
        
        Uses a list of polygons to generate sql to insert CollegePlan MULTIPOLYGON object.
        """
        locations = ['CollegeBoundary', 'OBlock', 'PBlock', 'Maintenance', 'Hothouse',
            'VanGarage', 'TractorShed', 'HBlockWest', 'HBlockNorth', 'HBlockSouth',
            'Administration', 'Busbay', 'Containers', 'ABlock', 'ABlockCloister',
            'BBlock', 'BBlockCloister', 'CBlock', 'CBlockCloister', 'Math', 'English',
            'Hall', 'TechGarage', 'GymGarage', 'HealthCentre']
        sql = SQL % ','.join([get_wkt(Location.objects.get(name=name).polygon)[8:] for name in locations])
        print(sql)
        return
