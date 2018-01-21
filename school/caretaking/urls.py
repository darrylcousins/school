__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.urls import re_path, path
from django.views.generic import TemplateView

from .views import StaffList, StaffDetail
from .views import DiaryList, DiaryDetail, DiaryAdd
from .views import DiaryEdit, DiaryDelete
from .views import TaskList, TaskAdd, TaskEdit, TaskDelete, TaskEditAjax
from .views import ProjectList, ProjectAdd

urlpatterns = (
    path('', StaffList.as_view(), name="staff-list"),

    # projects
    path('projects/',
        ProjectList.as_view(),
        name="project-list"),
    path('projects/add',
        ProjectAdd.as_view(),
        name="project-add"),

    # staff
    path('<str:username>/',
        StaffDetail.as_view(), name="staff-detail"),

    # diary
    path('<str:username>/diary/',
        DiaryList.as_view(),
        name="diary-list"),
    path('<str:username>/diary/add',
        DiaryAdd.as_view(),
        name="diary-add"),
    path('<str:username>/diary/<int:year>/<str:month>/<int:day>/<int:pk>/',
        DiaryDetail.as_view(),
        name="diary-detail"),
    path('<str:username>/diary/<int:year>/<str:month>/<int:day>/<int:pk>/edit',
        DiaryEdit.as_view(),
        name="diary-edit"),
    path('<str:username>/diary/<int:year>/<str:month>/<int:day>/<int:pk>/confirm-delete',
        DiaryDelete.as_view(),
        name="diary-confirm-delete"),

    # tasks
    path('<str:username>/tasks/',
        TaskList.as_view(),
        name="task-list"),
    path('<str:username>/tasks/add',
        TaskAdd.as_view(),
        name="task-add"),
    path('<str:username>/tasks/<int:pk>/edit',
        TaskEdit.as_view(),
        name="task-edit"),
    path('<str:username>/tasks/<int:pk>/edit/ajax',
        TaskEditAjax.as_view(),
        name="task-edit-ajax"),
    path('<str:username>/tasks/<int:pk>/delete',
        TaskDelete.as_view(),
        name="task-delete"),

)
