__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from graphene import relay, ObjectType, AbstractType, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from django.contrib.auth.models import User

from caretaking.models.task import Task
from caretaking.models.task import TaskType as MTaskType
from caretaking.models.staff import Staff


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = [
                'id',
                'username',
                'first_name',
                'last_name',
                'email',
                ]
        only_fields = [
                'id',
                'username',
                'first_name',
                'last_name',
                'email',
                ]
        interfaces = (relay.Node, )


class StaffType(DjangoObjectType):
    class Meta:
        model = Staff


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
    user = relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)
    all_staff = List(StaffType)
    all_tasks = List(TaskType)
    all_tasktypes = List(TaskTypeType)

    def resolve_all_staff(self, info, **kwargs):
        return Staff.objects.select_related('user').all()

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_all_tasks(self, info, **kwargs):
        return Task.objects.prefetch_related('tasktype').select_related('staff').all()

    def resolve_all_tasktypes(self, info, **kwargs):
        return TaskType.objects.all()
