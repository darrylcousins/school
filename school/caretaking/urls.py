__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.conf.urls import include, url
from django.views.generic import TemplateView

from .views import DiaryList
from .views import StaffDiaryList
from .views import DiaryDetail

urlpatterns = (
    url(r'^diaries/$', DiaryList.as_view()),
    url(r'^diaries/([\w-]+)/$', StaffDiaryList.as_view()),

    url(r'^diaries/(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/(?P<pk>[0-9]+)/$',
        DiaryDetail.as_view(),
        name="diary-detail"),

    # Examples:
    # url(r'^$', 'school.views.home', name='home'),
    # url(r'^school/', include('school.foo.urls')),

)
