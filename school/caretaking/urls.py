__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.conf.urls import include, url
from django.views.generic import TemplateView

from .views import StaffList, StaffDetail, DiaryList, DiaryDetail, TaskList

urlpatterns = (
    url(r'^$', StaffList.as_view(), name="caretaking"),
    url(r'^(?P<username>[\w-]+)/$', StaffDetail.as_view(), name="staff"),
    url(r'^diary/$', StaffList.as_view(), name="staff-list"),
    url(r'^(?P<username>[\w-]+)/diary/$', DiaryList.as_view(), name="staff-diary-list"),
    url(r'^(?P<username>[\w-]+)/tasks/$', TaskList.as_view(), name="staff-task-list"),

    url(r'^diary/(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/(?P<pk>[0-9]+)/$',
        DiaryDetail.as_view(),
        name="diary-detail"),

    # Examples:
    # url(r'^$', 'school.views.home', name='home'),
    # url(r'^school/', include('school.foo.urls')),

)
