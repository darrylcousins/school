__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import json

import graphene
from graphene import relay

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer, RefreshJSONWebTokenSerializer,
    VerifyJSONWebTokenSerializer
)

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


"""
Provides auth graphql queries used to use jws token authentication
"""

class TokenAuth(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)

    token = graphene.String(description="TWS authentication token")
    username = graphene.String(description="Username for user")
    uid = graphene.String(description="Id for user")


class TokenAuthInput(graphene.InputObjectType):
    """
    I'm seeing this as like the django form, defining field inputs

    As http://docs.graphene-python.org/en/latest/types/mutations/ says:

    `To use an InputField you define an InputObjectType that specifies the
    structure of your input data`
    """
    username = graphene.String(required=True)
    password = graphene.String(required=True)


class ValidateAuth(graphene.Mutation):
    class Arguments:
        data = TokenAuthInput(required=True)

    status = graphene.Int()
    token_auth = graphene.Field(TokenAuth)
    form_errors = graphene.String()

    @staticmethod
    def mutate(root, info, data=None):
        form = AuthenticationForm(data=data)
        if not form.is_valid():
            return CreateTokenAuth(
                    status=400,
                    form_errors=json.dumps(form.errors),
                    token_auth=None)

        return CreateTokenAuth(
                status=200,
                form_errors=None,
                token_auth=None)



class CreateTokenAuth(graphene.Mutation):
    class Arguments:
        data = TokenAuthInput(required=True)

    status = graphene.Int()
    token_auth = graphene.Field(TokenAuth)
    form_errors = graphene.String()
    username = graphene.String()
    uid = graphene.Int()

    @staticmethod
    def mutate(root, info, data=None):
        form = AuthenticationForm(data=data)
        if not form.is_valid():
            return CreateTokenAuth(
                    status=400,
                    form_errors=json.dumps(form.errors),
                    token_auth=None)

        serializer = JSONWebTokenSerializer(data=data)

        if serializer.is_valid():
            user = serializer.object.get('user') or info.context.user
            token = serializer.object.get('token')
        else:
            return CreateTokenAuth(
                    status=400,
                    form_errors=json.dumps({'user': 'no user found'}),
                    token_auth=None)

        token_auth = TokenAuth(token=token)
        return CreateTokenAuth(
                status=200,
                username=user.username,
                uid=user.id,
                token_auth=token_auth)


class Mutation(object):
    create_token_auth = CreateTokenAuth.Field()
    validate_auth = ValidateAuth.Field()
