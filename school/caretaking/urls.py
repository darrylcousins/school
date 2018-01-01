__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.conf.urls import include, url
from django.views.generic import TemplateView

from .views import StaffList, DiaryList, DiaryDetail

urlpatterns = (
    url(r'^diary/$', StaffList.as_view(), name="staff-list"),
    url(r'^diary/([\w-]+)/$', DiaryList.as_view(), name="diary-list"),

    url(r'^diary/(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/(?P<pk>[0-9]+)/$',
        DiaryDetail.as_view(),
        name="diary-detail"),

    # Examples:
    # url(r'^$', 'school.views.home', name='home'),
    # url(r'^school/', include('school.foo.urls')),

)
