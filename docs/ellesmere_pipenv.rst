Ellesmere pipenv install
========================

Have a go with pipenv to create environment::

    $ cd ~/.virtualenvs
    $ git clone https://github.com/cousinsd-ellesmere/school.git
    $ cd school
    $ C:\Users\cousinsd\AppData\Local\Continuum\Miniconda3\Scripts\virtualenv.exe .
    $ source bin/activate   <Scripts/activate>
    (school) $ pip install -r school/requirements.txt
    (school) $ pip install pipenv
    (school) $ 

Heroku (not cyberdelia!)::

    (school) $ heroku create --buildpack https://github.com/dschet/heroku-geo-buildpack.git ellesmere
    (school) $ heroku buildpacks:set heroku/python
    (school) $ heroku git:remote -a ellesmere
    (school) $ git push heroku master

Push from local database, this failed for me on windows so I created a local dump::

    $ PGUSER=ellesmere PGPASSWORD=ellesmere pg_dump  -Fc --no-acl --no-owner ellesmere > ellesmere.dump

And uploaded to S3 and then restored on heroku::

    $ heroku pg:backups:restore "https://s3-us-west-1.amazonaws.com/.../ellesmere.dump" DATABASE_URL

Which worked.
