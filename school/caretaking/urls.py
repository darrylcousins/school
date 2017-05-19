__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.conf.urls import include, url
from django.views.generic import TemplateView

from .views import DiaryList
from .views import StaffDiaryList
from .views import DiaryDetailView

urlpatterns = (
    url(r'^diaries/$', DiaryList.as_view()),
    url(r'^diaries/([\w-]+)/$', StaffDiaryList.as_view()),
    url(r'^diaries/diary/(?P<pk>[0-9]+)/$', DiaryDetailView.as_view(), name="diary-detail"),

    # Examples:
    # url(r'^$', 'school.views.home', name='home'),
    # url(r'^school/', include('school.foo.urls')),

)
