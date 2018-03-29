__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from .task import Query as TaskQuery
from .staff import Query as StaffQuery

"""
Module to gather all graphql query objects as the application endpoint.
"""

class Query(
        StaffQuery,
        TaskQuery
    ):
    pass


