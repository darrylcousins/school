__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import graphene

from caretaking.models.staff import Staff

from .staff import StaffType
from .update_staff import UpdateStaff

"""
Provides staff graphql queries
"""

class Query(object):

    all_staff = graphene.List(StaffType)

    def resolve_all_staff(self, info, **kwargs):
        return Staff.objects.select_related('user').all()


class Mutation(object):
    update_staff = UpdateStaff.Field()
