__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.contrib.auth.models import User

from graphene import relay, Field
from graphene_django.filter import DjangoFilterConnectionField

from .user import UserNode, UserType
from .create_user import CreateUser

"""
Provides user graphql queries, primarily to get current user
"""


class Query(object):

    user = relay.Node.Field(UserNode)

    def resolve_user(self, info, **kwargs):
        return User.objects.all().order_by('id')

    all_users = DjangoFilterConnectionField(UserNode)

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all().order_by('id')

    current_user = Field(UserType)

    def resolve_current_user(self, info, **kwargs):
        if not info.context.user.is_authenticated:
            return None
        return info.context.user


class Mutation(object):
    create_user = CreateUser.Field()
