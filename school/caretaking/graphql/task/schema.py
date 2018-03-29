__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from caretaking.models.task import Task
from caretaking.models.task import TaskType as MTaskType


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        exclude_fields = [
                'point',
            ]


class TaskTypeType(DjangoObjectType):
    class Meta:
        model = MTaskType


class Query(object):

    all_tasks = graphene.List(TaskType)
    all_tasktypes = graphene.List(TaskTypeType)

    def resolve_all_tasks(self, info, **kwargs):
        return Task.objects.prefetch_related('tasktype').select_related('staff').all()

    def resolve_all_tasktypes(self, info, **kwargs):
        return TaskType.objects.all()
