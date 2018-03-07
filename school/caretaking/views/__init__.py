__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from caretaking.views.staff import StaffDetail
from caretaking.views.staff import StaffList
from caretaking.views.diary import DiaryDetail
from caretaking.views.diary import DiaryList
from caretaking.views.diary import DiaryAdd
from caretaking.views.diary import DiaryEdit
from caretaking.views.diary import DiaryDelete
from caretaking.views.task import TaskList
from caretaking.views.task import TaskListAjax
from caretaking.views.task import TaskAdd
from caretaking.views.task import TaskEdit
from caretaking.views.task import TaskEditAjax
from caretaking.views.task import TaskDelete
from caretaking.views.task import TaskDetail
from caretaking.views.task import TodoList
from caretaking.views.project import ProjectAdd
from caretaking.views.project import ProjectDetail
from caretaking.views.project import ProjectList
from caretaking.views.project import ProjectEdit
from caretaking.views.project import ProjectDelete
from caretaking.views.project import ProjectConfirmDelete
from caretaking.views.photo import PhotoAdd
from caretaking.views.photo import PhotoDetail
from caretaking.views.photo import PhotoList
from caretaking.views.photo import PhotoDelete
from caretaking.views.photo import PhotoConfirmDelete
from caretaking.views.photo import PhotoUpload


__all__ = [
        'StaffDetail',
        'StaffList',
        'DiaryDetail',
        'DiaryList',
        'DiaryAdd',
        'DiaryEdit',
        'DiaryDelete',
        'TaskList',
        'TaskAdd',
        'TaskEdit',
        'TaskEditAjax',
        'TaskDelete',
        'TaskDetail',
        'TodoList',
        'ProjectAdd',
        'ProjectEdit',
        'ProjectDelete',
        'ProjectConfirmDelete',
        'ProjectDetail',
        'ProjectList',
        'PhotoAdd',
        'PhotoDetail',
        'PhotoDelete',
        'PhotoConfirmDelete',
        'PhotoList',
        'PhotoUpload',
        ]

