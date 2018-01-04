Ellesmere Django Install
========================

I struggled to have **pywin32** correctly installed in a python environment and usable with
**virtualenv**. Finally I deleted all python and went for **conda** to manage packages. Conda itself
includes pywin32 so I could then do::

        >>> import pythoncom

Using conda to set up a new environment::

        $ conda create --name ellesmere pywin32 django

Note that it was required to explicitly include ``pywin32``.

Activate the environment for local python::

        $ activate ellesemere
        (ellesmere)$

Deactivate with::

        $ deactivate

Install pyodbc and django-pyodbc-azure for odbc bindings::

        (ellesemere) $ pip install pyodbc
        (ellesemere) $ pip install django-pyodbc-azure

GeoDjango
---------

Due to failures trying to update to ``Django-2.0`` and further problems getting spatial
queries to work with modified ``pyodbc_gis`` I have decided to move to using `Postgres` for
`Windows` - the only drawback is that the `Metrel` package will no longer be available within the
same application (because Metrel database is only usable with `Metrel PatLink` with prebuilt `MSSql`
database. Any notes regarding `MSSql` installation have been moved to ``ellesmere_mssql.rst``.

I used `https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/#windows` to install
`Postgres`, `PostGIS`, `GDAL` and `GEOS` libraries. Briefly `OSGeo4W` installed the required packages.

Django supports PostgreSQL 10 with Psycopg 2.7.3.2 but I struggled with the installer when installing `PostGIS` extensions so instead I went of `9.6` and was able to install the extension.


Create Project
--------------

Standard getting started with ``django``::

        (ellesmere) $ cd path\to\conda\envs\ellesmere
        (ellesmere) $ django-admin startproject --template=https://github.com/twoscoops/django-twoscoops-project/zipball/master --extension=py,rst,html school
        (ellesmere) $ cd school
        (ellesmere) $ vi school/settings.py

'path\to\conda\envs' in my case matches 'C:\Users\cousinsd\AppData\Local\Continuum\Miniconda3\envs\'.        

Now we can start the server without connection errors::

        (ellesmere) $ python manage.py runserver
        Performing system checks...

        System check identified no issues (0 silenced). 
        March 19, 2017 - 10:39:07
        Django version 1.10.5, using settings 'school.settings'
        Starting development server at http://127.0.0.1:8000/

Stop/stop Postgresql
--------------------

The server Ellesmere for example::

    $ net start|stop 'SQL Server (ELLESMERE)'
    $ net start|stop 'SQL Server (METREL)'

Grepping the powershell way
---------------------------

In current directory::

    $ ls * -filter *.py | sls 'string to search'

Recursively::

    $ ls * -r -filter *.py | sls 'string to search'

Using Django Extensions
-----------------------

To use django model to uml then graphviz is required. ``http://www.graphviz.org``. MSI installer worked fine. 

But quickly then noted that pygraphviz only works to python-2.7 so gave up.

May still install the extensions for the ``shell_plus`` command.

