__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.urls import re_path, path
from django.views.generic import TemplateView

from .views import StaffList, StaffDetail
from .views import DiaryList, DiaryDetail, TaskList

urlpatterns = (
    #url(r'^$', StaffList.as_view(), name="caretaking"),
    path('', StaffList.as_view(), name="caretaking"),
    path('diary/', StaffList.as_view(), name="staff-list"),

    path('diary/<int:year>/<str:month>/<int:day>/<int:pk>/',
        DiaryDetail.as_view(),
        name="diary-detail"),
    path('<str:username>/diary/',
        DiaryList.as_view(),
        name="staff-diary-list"),
    path('<str:username>/tasks/',
        TaskList.as_view(),
        name="staff-task-list"),
    path('<str:username>/',
        StaffDetail.as_view(), name="staff-detail"),

)
