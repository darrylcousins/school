__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import json

import graphene

from school.caretaking.forms import StaffCreationForm


class StaffInput(graphene.InputObjectType):
    """
    Specifies the structure of a user.
    """
    title = graphene.String(required=True)
    first_name = graphene.String(required=False)
    last_name = graphene.String(required=False)
    email = graphene.String(required=True)
    comment = graphene.String(required=False)


