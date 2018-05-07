__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import json

from django.contrib.auth.forms import UserCreationForm

import graphene

# import definitions
class UserInput(graphene.InputObjectType):
    """
    Specifies the structure of a user.
    """
    username = graphene.String(required=True)
    password1 = graphene.String(required=True)
    password2 = graphene.String(required=True)


# mutation definitions
class CreateUser(graphene.Mutation):

    # the input
    class Arguments:
        data = UserInput(required=True)

    # what gets returned
    status = graphene.Int()
    form_errors = graphene.String()
    username = graphene.String()
    uid = graphene.Int()

    @staticmethod
    def mutate(root, info, data=None):
        form = UserCreationForm(data=data)
        if not form.is_valid():
            return CreateUser(
                    status=400,
                    form_errors=json.dumps(form.errors),
                    )
        user = form.save()
        return CreateUser(
                status=200,
                username=user.username,
                uid=user.id,
                )
