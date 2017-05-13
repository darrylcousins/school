Ellesmere Django Install
========================

I struggled to have **pywin32** correctly installed in a python environment and usable with
**virtualenv**. Finally I deleted all python and went for **conda** to manage packages. Conda itself
includes pywin32 so I could then do::

        >>> import pythoncom

Using conda to set up a new environment::

        $ conda create --name ellesmere pywin32 django

Note that it was required to explicitly include ``pywin32``.

Install pyodbc and django-pyodbc-azure for odbc bindings::

        (ellesemere) $ pip install pyodbc
        (ellesemere) $ pip install django-pyodbc-azure

GeoDjango
---------

I found `django_pyodbc_gis` but this package is oldish and does not work with django 1.11 so using
it a base I made `pyodbc_gis` to provide a database backend to support GeoDjango. Still a work in
progress but serving it's purpose for now.

Watch the ``ODBC SQL type -151 is not yet supported`` error, this has in every case been when I'm
selecting a ``geometry`` field and forgetting to append ``STAsText()``.

`GDAL` and `GEOS` libraries are required, see
`https://docs.djangoproject.com/en/1.11/ref/contrib/gis/install/#windows` for further information
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
