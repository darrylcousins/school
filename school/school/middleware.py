__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.utils.deprecation import MiddlewareMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class JWTMiddleware(MiddlewareMixin):

    def process_request(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '')
        #print("HTTP TOKEN: ", token)
        if not token.startswith('JWT'):
            return
        jwt_auth = JSONWebTokenAuthentication()
        auth = None
        try:
            auth = jwt_auth.authenticate(request)
        except Exception as e:
            print("EXCEPTION", e)
            return

        request.user = auth[0]
        #print("authenticated user: ", request.user)
        #print(request)
