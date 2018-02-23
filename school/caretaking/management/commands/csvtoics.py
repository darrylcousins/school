__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import tempfile, os
import csv
from datetime import datetime
import pytz
from pprint import PrettyPrinter

from django.core.management.base import BaseCommand, CommandError

from icalendar import Calendar, Event, vDatetime, vText

def display(cal):
    return cal.to_ical().replace('\r\n', '\n').strip()

class Command(BaseCommand):
    """
    Convert Deb's spreadsheet to ics file to import to google calendar

    """
    help = "Create ics from comma delimited csv files as exported from google spreadsheet data"

    def handle(self, *args, **options):
        """Lazy no error checking, relies on good collection of data.
        """
        cal = Calendar()
        cal.add('prodid', '-//cousinsd/ellesmerecal//NONSGML v1.0//EN')
        cal.add('version', '2.0')

        reader = csv.reader(open('caretaking/data/ellesmere-hall-2.csv'), delimiter=',')
        count = 0
        for row in reader:
            description = row[2]
            if not description:
                continue

            tmp = row[0]
            if tmp:
                day = tmp

            times = row[3]
            if times:
                (start, end) = times.split('-')

                sub = end[-2:]
                if start[0] > end [0]:
                    sub = 'am'
                end = day + ' ' + end
                start = day + ' ' + start + sub
                try:
                    end = datetime.strptime(end, '%d.%m.%y %I.%M%p')
                except ValueError:
                    end = datetime.strptime(end, '%d.%m.%y %I%p')
                try:
                    start = datetime.strptime(start, '%d.%m.%y %I.%M%p')
                except ValueError:
                    start = datetime.strptime(start, '%d.%m.%y %I%p')
                print(start, end)
                print(description)
                event = Event()
                event.add('summary', vText(description))
                event.add('dtstamp', start)
                event.add('dtstart', start)
                event.add('dtend', end)
                cal.add_component(event)

        #directory = tempfile.mkdtemp()
        #f = open(os.path.join(directory, 'example.ics'), 'wb')
        f = open('caretaking/data/ellesmere-hall-2.ics', 'wb')
        f.write(cal.to_ical())
        f.close()
        return

