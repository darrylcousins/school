__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.urls import re_path, path
from django.views.generic import TemplateView

from .views import StaffList, StaffDetail
from .views import DiaryList, DiaryDetail, TaskList

urlpatterns = (
    #url(r'^$', StaffList.as_view(), name="caretaking"),
    path('', StaffList.as_view(), name="caretaking"),
    path('diary/', StaffList.as_view(), name="staff-list"),

    re_path('(?P<username>[\w-]+)/',
        StaffDetail.as_view(), name="staff"),
    re_path('(?P<username>[\w-]+)/diary/',
        DiaryList.as_view(),
        name="staff-diary-list"),
    re_path('(?P<username>[\w-]+)/tasks/',
        TaskList.as_view(),
        name="staff-task-list"),

    re_path('diary/(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/(?P<pk>[0-9]+)/',
        DiaryDetail.as_view(),
        name="diary-detail"),

    # Examples:
    # url(r'^$', 'school.views.home', name='home'),
    # url(r'^school/', include('school.foo.urls')),

)
