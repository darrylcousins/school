Load Data
=========

Bit of bother loading fixtures from json files created with dumpdata.

Got the encoding problems to work by hacking django.core.management.loaddata to use ``tokenize``::

    >>> import tokenize
    >>> f = tokenize.open(path)

And also needed to open the json file in Notepad and save as UTF-8.

Surely a better solution to this problem.

Locations
=========

I have created the location polygons using Google Earth, copy/saving kml files for each polygon.
Then using a script run in Visual Studio I create location.sql which is run with::

     $ sqlcmd -S R940_DARRYL\ELLESMERE -i location.sql

From these I have a django management script to build an run sql to create a multipoint polygon
representing the school plan (SchoolPlan)::

    $ python manage.py mkcollege > college.sql

Which can then be added with::

     $ sqlcmd -S R940_DARRYL\ELLESMERE -i college.sql

Staff
=====

Base staff data can be loaded from ``caretaking/fixtures/staff.json``::

    $ python manage.py loaddata (--app caretaking) staff

Diary Data
==========

Older diary data can be loaded using the ``importdiary`` management command. It uses tab delimited
``csv`` files exported from google spreadsheets.::

    $ python manage.py importdiary

Adding Location and TaskType and Duration to Tasks
==================================================

This will be done by hand.

