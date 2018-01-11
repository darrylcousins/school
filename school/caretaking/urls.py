__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.urls import re_path, path
from django.views.generic import TemplateView

from .views import StaffList, StaffDetail
from .views import DiaryList, DiaryDetail, DiaryAdd, DiaryEdit
from .views import TaskList, TaskAdd
from .views import ProjectList, ProjectAdd

urlpatterns = (
    #url(r'^$', StaffList.as_view(), name="caretaking"),
    path('', StaffList.as_view(), name="caretaking"),
    path('diary/', StaffList.as_view(), name="staff-list"),

    path('diary/<int:year>/<str:month>/<int:day>/<int:pk>/',
        DiaryDetail.as_view(),
        name="diary-detail"),
    path('diary/<int:year>/<str:month>/<int:day>/<int:pk>/edit',
        DiaryEdit.as_view(),
        name="diary-edit"),
    path('projects/',
        ProjectList.as_view(),
        name="project-list"),
    path('projects/add',
        ProjectAdd.as_view(),
        name="project-add"),
    path('<str:username>/diary/add',
        DiaryAdd.as_view(),
        name="diary-add"),
    path('<str:username>/diary/',
        DiaryList.as_view(),
        name="diary-list"),
    path('<str:username>/tasks/add',
        TaskAdd.as_view(),
        name="task-add"),
    path('<str:username>/tasks/',
        TaskList.as_view(),
        name="task-list"),
    path('<str:username>/',
        StaffDetail.as_view(), name="staff-detail"),

)
