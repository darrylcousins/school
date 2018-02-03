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
from caretaking.views.project import ProjectAdd
from caretaking.views.project import ProjectDetail
from caretaking.views.project import ProjectList
from caretaking.views.project import ProjectEdit
from caretaking.views.project import ProjectDelete


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
        'ProjectAdd',
        'ProjectEdit',
        'ProjectDelete',
        'ProjectDetail',
        'ProjectList'
        ]

