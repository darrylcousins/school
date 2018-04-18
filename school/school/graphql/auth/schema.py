__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from .token import CreateTokenAuth
from .token import ValidateAuth

class Mutation(object):
    create_token_auth = CreateTokenAuth.Field()
    validate_auth = ValidateAuth.Field()
