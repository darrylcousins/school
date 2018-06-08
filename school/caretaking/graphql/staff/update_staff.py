__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import json

import graphene

from caretaking.forms import StaffUpdateForm


# input definitions
class StaffInput(graphene.InputObjectType):
    """
    Specifies the structure of a user.
    """
    username = graphene.String(required=True)
    title = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    comment = graphene.String(required=False)


# mutation definitions
class UpdateStaff(graphene.Mutation):
    """react-apollo:

        const M = gql`
          mutation {
              updateStaff(
                data: {
                  username: "${ data["username"] }",
                  title: "${ data["title"] }",
                  first_name: "${ data["first_name"] }",
                  last_name: "${ data["last_name"] }",
                  email: "${ data["email"] }",
                  comment: "${ data["comment"] }",
                  }
                )
              {
              status
              formErrors
              username
              uid
            }
          }
        `
    """

    # the input
    class Arguments:
        data = StaffInput(required=True)

    # what gets returned
    status = graphene.Int()
    form_errors = graphene.String()
    username = graphene.String()
    uid = graphene.Int()

    @staticmethod
    def mutate(root, info, data=None):
        form = StaffUpdateForm(data=data)
        if not form.is_valid():
            return UpdateStaff(
                    status=400,
                    form_errors=json.dumps(form.errors),
                    )
        staff = form.save()
        return UpdateStaff(
                status=200,
                username=staff.user.username,
                uid=staff.id,
                )
