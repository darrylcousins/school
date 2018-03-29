__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from caretaking.models.staff import Staff


class StaffType(DjangoObjectType):
    class Meta:
        model = Staff


class Query(object):

    all_staff = graphene.List(StaffType)

    def resolve_all_staff(self, info, **kwargs):
        return Staff.objects.select_related('user').all()
