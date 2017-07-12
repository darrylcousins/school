__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.conf.urls import include, url
from django.views.generic import TemplateView

from .views import ApplianceList, JSONApplianceList

urlpatterns = (
    url(r'^appliances/$', ApplianceList.as_view(), name="appliance-list"),
    url(r'^appliances/ajax$', JSONApplianceList.as_view(), name="json-appliance-list"),

    # Examples:
    # url(r'^$', 'school.views.home', name='home'),
    # url(r'^school/', include('school.foo.urls')),

)

