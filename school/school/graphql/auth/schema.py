__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import graphene
from graphene import relay

from django.contrib.auth.models import User

"""
Provides auth graphql queries used to use jws token authentication
"""

class TokenAuthType(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)

    token = graphene.String(description="TWS authentication token")


class Query(object):

    auth = graphene.Field(TokenAuthType)

    def resolve_auth(self, info, **kwargs):
        auth = TokenAuthType(token='JWS authtoken')
        return auth
