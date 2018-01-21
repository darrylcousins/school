__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from caretaking.views.staff import StaffDetail
from caretaking.views.staff import StaffList
from careteking.views.diary import DiaryDetail
from careteking.views.diary import DiaryList
from careteking.views.diary import DiaryAdd
from careteking.views.diary import DiaryEdit
from careteking.views.diary import DiaryDelete
from careteking.views.task import TaskList
from careteking.views.task import TaskAdd
from careteking.views.task import TaskEdit
from careteking.views.task import TaskEditAjax
from careteking.views.task import TaskDelete
from careteking.views.project import ProjectAdd
from careteking.views.project import ProjectList

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
        'ProjectList'
        ]

