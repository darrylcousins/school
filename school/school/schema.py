__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'


import graphene

import caretaking.schema


class Query(caretaking.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(query=Query)
