Ellesmere Django Install
========================

Notes made while getting django to work with `MSSql` required for the `Metrel` database.

GeoDjango
---------

I found `django_pyodbc_gis` but this package is oldish and does not work with django 1.11 so using
it a base I made `pyodbc_gis` to provide a database backend to support GeoDjango. Still a work in
progress but serving it's purpose for now.

Watch the ``ODBC SQL type -151 is not yet supported`` error, this has in every case been when I'm
selecting a ``geometry`` field and forgetting to append ``STAsText()``.

`GDAL` and `GEOS` libraries are required, see
`https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/#windows` for further information
to install `OSGeo4W` which will install the required packages.

Create Project
--------------

Standard getting started with ``django``::

        (ellesmere) $ cd path\to\conda\envs\ellesmere
        (ellesmere) $ django-admin startproject --template=https://github.com/twoscoops/django-twoscoops-project/zipball/master --extension=py,rst,html school
        (ellesmere) $ cd school
        (ellesmere) $ vi school/settings.py

'path\to\conda\envs' in my case matches 'C:\Users\cousinsd\AppData\Local\Continuum\Miniconda3\envs\'.        

Had a wee bit of trouble getting the database settings correct to connect to **SQL Server (2012)**
but by digging around with **SQL Server Management Studio** and **SQL Server Configuration Manager**
I figured out the following settings (after having created the database ``ellesmere`` in
**Management Studio**)::

        DATABASES = {
            'default': {
                'ENGINE': 'sql_server.pyodbc',
                'NAME': 'ellesmere',
                'HOST':'R940_DARRYL\ELLESMERE',
                'OPTIONS':  {'driver': 'ODBC Driver 13 for SQL Server'}
            }
        }

Now we can start the server without connection errors::

        (ellesmere) $ python manage.py runserver
        Performing system checks...

        System check identified no issues (0 silenced). 
        March 19, 2017 - 10:39:07
        Django version 1.10.5, using settings 'school.settings'
        Starting development server at http://127.0.0.1:8000/

``USER`` defines the name of the user to use when authenticating to the server. When empty, a trusted
connection (SSPI) will be used. But for full write permissions I used my computer user name and
password (only for development).

Stop/stop sql servers
---------------------

The server Ellesmere for example::

    $ net start|stop 'SQL Server (ELLESMERE)'
    $ net start|stop 'SQL Server (METREL)'

Using Django Extensions
-----------------------

To use django model to uml then graphviz is required. ``http://www.graphviz.org``. MSI installer worked fine. 

But quickly then noted that pygraphviz only works to python-2.7 so gave up.

May still install the extensions for the ``shell_plus`` command.

Get test fixture for Metrel database
------------------------------------

::
        $ python manage.py dumpdata --database=metrel -e contenttypes -e auth.permission -e auth.group -e auth.user -e sessions -e sites -e admin -e caretaking -e metrel.appinfo -e metrel.translations --indent 4 > metrel\fixtures\initial.json

Skip ``translations`` and ``appinfo`` because ``id`` not allowed (in migrations?).

Django 2
--------

Upgrade failed due to sql_server.pydboc - pin Django==1.10.8 for now. Without Metrel perhaps
consider migration to postgres.

