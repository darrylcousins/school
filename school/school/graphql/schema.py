__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import graphene
from graphene import relay

from caretaking.graphql.schema import Query as CaretakingQuery

from .auth import Query as AuthQuery
from .user import Query as UserQuery

"""
Module to gather all graphql query objects as the application endpoint.
"""

class Query(
        CaretakingQuery,
        AuthQuery,
        UserQuery,
        graphene.ObjectType
    ):
    pass


schema = graphene.Schema(query=Query)
