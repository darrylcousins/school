__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.contrib.contenttypes.models import ContentType
from django.http.request import QueryDict

from caretaking.models.photo import Photo


class PhotoEnabled:

    def get_photos(self):
        model= ContentType.objects.get_for_model(self)
        model_str = '.'.join((model.app_label, model.name.lower()))
        photos = Photo.objects.filter(model=model_str, model_pk=self.pk)
        return photos

    def urlencode_ct(self):
        model= ContentType.objects.get_for_model(self)
        model_str = '.'.join((model.app_label, model.name.lower()))
        qd = QueryDict('model=' + model_str + '&model_pk=' + str(self.pk))
        return qd.urlencode()
