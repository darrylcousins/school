__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

# enable the admin:
from django.contrib import admin
admin.autodiscover() # this may be obsolete in Django-2
admin.site.site_header = 'caretaking@ellesmere'

urlpatterns = (
    path('', TemplateView.as_view(template_name='base.html'), name='index'),
    path('caretaking/', include('caretaking.urls')),

    path('admin/', admin.site.urls),
)
