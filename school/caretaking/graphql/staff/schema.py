__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import graphene

from caretaking.models.staff import Staff

from .staff import StaffType

class Query(object):

    all_staff = graphene.List(StaffType)

    def resolve_all_staff(self, info, **kwargs):
        return Staff.objects.select_related('user').all()
