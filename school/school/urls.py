__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

from school.graphql import schema

# enable the admin:
from django.contrib import admin
admin.autodiscover() # this may be obsolete in Django-2
admin.site.site_header = 'caretaking@ellesmere'

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='index'),
    path('caretaking/', include('caretaking.urls')),

    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
#    path('gql', csrf_exempt(GraphQLView.as_view(batch=True, schema=schema))),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

