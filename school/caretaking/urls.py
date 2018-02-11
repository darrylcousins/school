__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.urls import re_path, path
from django.views.generic import TemplateView

from .views import StaffList, StaffDetail
from .views import DiaryList, DiaryDetail, DiaryAdd
from .views import DiaryEdit, DiaryDelete
from .views import TaskList, TaskAdd, TaskEdit, TaskDelete
from .views import TaskDetail, TaskEditAjax, TaskListAjax
from .views import ProjectList, ProjectAdd, ProjectDetail
from .views import ProjectEdit, ProjectDelete, ProjectConfirmDelete
from .views import PhotoAdd, PhotoList, PhotoDetail, PhotoDelete, PhotoConfirmDelete

urlpatterns = (
    path('', StaffList.as_view(), name="staff-list"),

    # projects
    path('projects/',
        ProjectList.as_view(),
        name="project-list"),
    path('projects/add',
        ProjectAdd.as_view(),
        name="project-add"),
    path('projects/<int:pk>',
        ProjectDetail.as_view(),
        name="project-detail"),
    path('projects/<int:pk>/edit',
        ProjectEdit.as_view(),
        name="project-edit"),
    path('projects/<int:pk>/delete',
        ProjectDelete.as_view(),
        name="project-delete"),
    path('projects/<int:pk>/confirm-delete',
        ProjectConfirmDelete.as_view(),
        name="project-confirm-delete"),

    # photos
    path('photos/add',
        PhotoAdd.as_view(),
        name="photo-add"),
    path('photos',
        PhotoList.as_view(),
        name="photo-list"),
    path('photos/<int:pk>',
        PhotoDetail.as_view(),
        name="photo-detail"),
    path('photos/<int:pk>/edit',
        PhotoDetail.as_view(),
        name="photo-edit"),
    path('photos/<int:pk>/delete',
        PhotoDelete.as_view(),
        name="photo-delete"),
    path('photos/<int:pk>/confirm-delete',
        PhotoConfirmDelete.as_view(),
        name="photo-confirm-delete"),

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
    path('<str:username>/tasks/ajax',
        TaskListAjax.as_view(),
        name="task-list-ajax"),
    path('<str:username>/tasks/add',
        TaskAdd.as_view(),
        name="task-add"),
    path('<str:username>/tasks/<int:pk>',
        TaskDetail.as_view(),
        name="task-detail"),
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
