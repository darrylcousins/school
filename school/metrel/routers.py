__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

class MetrelRouter(object):
    """A router to control all database operations on models in the metrel application

    Ensures that metrel models are accessed from the `metrel` database and not `default`.

    Requires that a database named 'metrel' is defined in settings.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'metrel':
            return 'metrel'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'metrel':
            return 'metrel'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'metrel' or obj2._meta.app_label == 'metrel':
            return True
        return None

    def allow_syncdb(self, db, model):
        if db == 'metrel':
            return model._meta.app_label == 'metrel'
        elif model._meta.app_label == 'metrel':
            return False
        return None
