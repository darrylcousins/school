__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from graphene_django.views import GraphQLView

from school.schema import schema

# enable the admin:
from django.contrib import admin
admin.autodiscover() # this may be obsolete in Django-2
admin.site.site_header = 'caretaking@ellesmere'

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='index'),
    path('caretaking/', include('caretaking.urls')),

    path('graphql', GraphQLView.as_view(graphiql=True, schema=schema)),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

