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

Heroku::

    (school) $ heroku create --buildpack https://github.com/cyberdelia/heroku-geo-buildpack.git ellesmere
    (school) $ heroku buildpacks:set heroku/python
    (school) $ heroku git:remote -a ellesmere
    (school) $ git push heroku master
