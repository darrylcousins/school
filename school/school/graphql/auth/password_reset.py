__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import json

import graphene
from graphene import relay

from django.forms import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm


# input definitions
class PasswordResetInput(graphene.InputObjectType):
    """
    Specifies the structure of a user.
    """
    email = graphene.String(required=True)


# mutation definitions
class PasswordReset(graphene.Mutation):
    """react-apollo:

        const M = gql`
          mutation {
              passwordReset(
                data: {
                  email: "${ data["email"] }",
                  }
                )
              {
              status
              formErrors
              email
            }
          }
        `
    """

    # the input
    class Arguments:
        data = PasswordResetInput(required=True)

    # what gets returned
    status = graphene.Int()
    form_errors = graphene.String()
    email = graphene.String()

    @staticmethod
    def mutate(root, info, data=None):
        form = PasswordResetForm(data=data)
        if not form.is_valid():
            return PasswordReset(
                    status=400,
                    form_errors=json.dumps(form.errors),
                    )
        try:
            # PasswordResetForm.save() checks for the user and sends email with token'd link
            # requires template: `registration/password_reset_email.html`
            # requires template: `registration/password_reset_subject.html`
            form.save()
            return PasswordReset(
                    status=200,
                    email=form.cleaned_data['email'],
                    )
        except ValidationError as error:
            return PasswordReset(
                    status=400,
                    form_errors=json.dumps(error),
                    )
