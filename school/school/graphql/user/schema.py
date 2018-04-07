__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import graphene
from graphene import relay

from django.contrib.auth.models import User

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

"""
Provides user graphql queries, primarily to get current user
"""


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
                'staff',
                ]
        interfaces = (relay.Node, )


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(object):

    #user = relay.Node.Field(UserNode)

    all_users = DjangoFilterConnectionField(UserNode)

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    current_user = graphene.Field(UserType)

    def resolve_current_user(self, info, **kwargs):
        if not info.context.user.is_authenticated:
            return None
        return info.context.user
