__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.contrib.auth.models import User

from graphene import relay
from graphene_django import DjangoObjectType

"""
Provides user node and type, primarily to get current user
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
