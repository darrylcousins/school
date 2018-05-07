__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from graphene_django import DjangoObjectType

from caretaking.models.staff import Staff


class StaffType(DjangoObjectType):
    class Meta:
        model = Staff

