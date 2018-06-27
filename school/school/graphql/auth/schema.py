__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from .token import CreateTokenAuth
from .token import ValidateAuth
from .password_reset import PasswordReset

class Mutation(object):
    create_token_auth = CreateTokenAuth.Field()
    validate_auth = ValidateAuth.Field()
    password_reset = PasswordReset.Field()
