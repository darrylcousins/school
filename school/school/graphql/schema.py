__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import graphene
from graphene import relay

from graphene_django.debug import DjangoDebug


from caretaking.graphql import Query as CaretakingQuery
from caretaking.graphql import Mutation as StaffMutation

from .auth import Mutation as TokenAuthMutation
from .user import Query as UserQuery
from .user import Mutation as UserMutation

"""
Module to gather all graphql query objects as the application endpoint.
"""

class Mutations(
    TokenAuthMutation,
    UserMutation,
    StaffMutation,
    graphene.ObjectType,
):
    pass


class Query(
        CaretakingQuery,
        UserQuery,
        graphene.ObjectType
    ):
    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=Query, mutation=Mutations)
