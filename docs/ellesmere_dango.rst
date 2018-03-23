Ellesmere Django Install
========================

I struggled to have **pywin32** correctly installed in a python environment and usable with
**virtualenv**. Finally I deleted all python and went for **conda** to manage packages. Conda itself
includes pywin32 so I could then do::

        >>> import pythoncom

Using conda to set up a new environment::

        $ conda create --name ellesmere pywin32 django

Note that it was required to explicitly include ``pywin32``.

I'm using `conemu` for shell sessions. While `Powershell` is more useful and powerful for command
line work the simple `cmd` session is required to work with the activated environment.

Activate the environment for local python::

        $ activate ellesemere
        (ellesmere)$

Deactivate with::

        (ellesmere)$ deactivate

Packages
--------

Install packages::

        (ellesmere)$ pip install -r requirements/base.txt

This installs all the packages listed below.  ::

        (ellesmere)$ pip install -U django
        (ellesmere)$ pip install -U matplotlib
        (ellesmere)$ pip install -U palettable

Note that packages can also be installed using conda e.g.::

        (ellesmere)$ conda install -c conda-forge wordcloud

Note: I had a fair bit of trouble installing ``wordcloud`` because win32/python3.6 conda package
not available. Finally managed with a pip install which then meant installing C++ build tools and
copying files to make it all come together.

Note: On fedora I also needed::

        $ sudo dnf install gcc
        $ sudo dnf install redhat-rpm-config
        $ sudo dnf install python3-devel
        $ sudo dnf install python3-lxml

GeoDjango
---------

Due to failures trying to update to ``Django-2.0`` and further problems getting spatial
queries to work with modified ``pyodbc_gis`` I have decided to move to using `Postgres` for
`Windows` - the only drawback is that the `Metrel` package will no longer be available within the
same application (because Metrel database is only usable with `Metrel PatLink` with prebuilt `MSSql`
database. Any notes regarding `MSSql` installation have been moved to ``ellesmere_mssql.rst``.

Data Visualisation
------------------

Went with these packages::

        (ellesmere)$ pip install pandas
        (ellesmere)$ pip install plotly

I used `https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/#windows` to install
`Postgres`, `PostGIS`, `GDAL` and `GEOS` libraries. Briefly `OSGeo4W` installed the required packages.

Django supports PostgreSQL 10 with Psycopg 2.7.3.2 but I struggled with the installer when installing `PostGIS` extensions so instead I went of `9.6` and was able to install the extension. Later with Fedora27 it defaulted in any case to 9.6.8 at time of installation. I followed `https://fedoraproject.org/wiki/PostgreSQL` for postgres install and setup on Fedora27.

And then on fedora things got a little complicated when I found the heroku is postgresql10 and fedora at postgresql9. I followed `https://www.if-not-true-then-false.com/2012/install-postgresql-on-fedora-centos-red-hat-rhel/` to get a repository with postgresql10 and then could::

        $ sudo dnf install postgres10
        $ sudo dnf install postgis24_10 # version matched in same repository

Not to forget initialisation::

        $ sudo /usr/pgsql-10/bin/postgresql-10-setup initdb

The later nicely install all gdal and gis packages. Stop and start postgres with::

        $ sudo systemctl enable postgresql-10.service
        $ sudo systemctl start postgresql-10.service

Create Database
---------------

Install Heroku
``````````````

        ::
        $ npm install heroku

Get Current Database
````````````````````

If we are still on heroku and that is the most recent database then do::

        $ su - postgres
        $ heroku pg:pull HEROKU_POSTGRESQL_AMBER ellesmere --app ellesmere

Otherwise
`````````

Create the database and user using `postgres` superuser and set some defaults::

        $ sudo su - postgres
        $ psql
        postgres=# CREATE USER ellesmere PASSWORD 'ellesmere';
        postgres=# CREATE DATABASE ellesmere OWNER ellesmere;
        postgres=# ALTER ROLE ellesmere SET client_encoding TO 'utf8';
        postgres=# ALTER ROLE ellesmere SET default_transaction_isolation TO 'read committed';
        postgres=# ALTER ROLE ellesmere SET timezone TO 'Pacific/Auckland';
        postgres=# GRANT ALL PRIVILEGES ON DATABASE ellesmere TO ellesmere;

Superuser status is required to run `CREATE EXTENSION`::

        postgres=# ALTER ROLE ellesmere WITH SUPERUSER;
        postgres=# \c ellesmere
        ellesmere=# CREATE EXTENSION postgis;
        postgres=# \q


Create Project
--------------

This getting started section applies to new projects only.

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

Create tables
-------------

If we have changed model definitions then new migrations need to be created::

        (ellesmere) $ python manage.py makemigrations caretaking

Use ``migrate`` to create the tables in new database::

        (ellesmere) $ python manage.py migrate

Install fixtures
----------------

With fixtures and sql some initial data can be imported into the database.::

        (ellesmere) $ python manage.py loaddata location
        (ellesmere) $ python manage.py loaddata staff
        (ellesmere) $ python manage.py loaddata tasktype

Or create superuser a staff member::

        (ellesmere) $ python manage.py createsuperuser

College Multipolygon
--------------------

This is the multipolygon mapped onto maps to identify school. **If the location fixture is up to date
then the following steps will not be necessary.**

Run ``mkcollege`` to construct sql for mulitpolygon college location (only necessary if the polygon
locations have changed)::

        (ellesmere) $ python manage.py mkcollege > caretaking/sql/college.sql

And import::

        $ psql -U ellesmere -d ellesmere -a -f college.sql

Import spreadsheet records (uses csv file in caretaking/data/oct_current.csv)::

        (ellesmere) $ python manage.py importdiary

Stop/stop Postgresql
--------------------

The server Ellesmere for example::

    $ TODO

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

