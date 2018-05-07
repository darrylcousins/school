Authentication
==============

In the work to make a frontend using `react`_ and `apollo`_ `JWT Authentication`
was chosen to maintain authentication using a `JWT Token` in the headers.

JWT install
-----------

`django-rest-framework-jwt`_ and `django-cors-headers`_ are used to provide
functionality (``cors-headers`` are used to allow cross domain requests)::

  pip install djangorestframework
  pip install djangorestframework-jwt
  pip install django-cors-headers

Settings
--------

Add to ``INSTALLED APPS``::

  INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
    'graphene_django',
    ...
  ]

And ``MIDDLEWARE_CLASSES``, note the custom ``JWTMiddleware``, more on this below::

  MIDDLEWARE = [
      'django.middleware.security.SecurityMiddleware',
      'django.contrib.sessions.middleware.SessionMiddleware',
      'corsheaders.middleware.CorsMiddleware',
      'django.middleware.common.CommonMiddleware',
      'django.middleware.csrf.CsrfViewMiddleware',
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      'school.middleware.JWTMiddleware',
      'django.contrib.messages.middleware.MessageMiddleware',
      'django.middleware.clickjacking.XFrameOptionsMiddleware',
      'whitenoise.middleware.WhiteNoiseMiddleware',
  ]

Other settings used here are, with some notes that show that these are still in
development::

  # need to work out a better way for production
  CORS_ORIGIN_ALLOW_ALL = True

  # jwt rest framework configuration for frontend
  REST_FRAMEWORK = {
      'DEFAULT_PERMISSION_CLASSES': (
          'rest_framework.permissions.IsAuthenticated',
      ),
      'DEFAULT_AUTHENTICATION_CLASSES': (
          'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
          # no session authentication?
          #'rest_framework.authentication.SessionAuthentication',
          'rest_framework.authentication.BasicAuthentication',
      ),
  }

  # never expires - fix for production
  JWT_AUTH = {
      'JWT_EXPIRATION_DELTA': datetime.timedelta(days=3),
  }

Middleware
----------

School JWT ``middleware.py``::

  from django.utils.deprecation import MiddlewareMixin
  from rest_framework_jwt.authentication import JSONWebTokenAuthentication


  class JWTMiddleware(MiddlewareMixin):

      def process_request(self, request):
          token = request.META.get('HTTP_AUTHORIZATION', '')
          if not token.startswith('JWT'):
              return
          jwt_auth = JSONWebTokenAuthentication()
          auth = None
          try:
              auth = jwt_auth.authenticate(request)
          except Exception as e:
              return

          request.user = auth[0]

Graphql
-------

School uses a graphql `mutation`_ to validate form data and create the token.
Validation is done with the `django.contrib.auth` form::

  form = AuthenticationForm(data=data)

  if not form.is_valid():
      return CreateTokenAuth(
              status=400,
              form_errors=json.dumps(form.errors),
              token_auth=None)

`rest_framework_jwt.serializers` to verify the user and create a token::

  serializer = JSONWebTokenSerializer(data=data)

  if serializer.is_valid():
      user = serializer.object.get('user') or info.context.user
      token = serializer.object.get('token')

This token is returned to the frontend and saved in a state store using Apollo Client.

.. _react: https://reactjs.org
.. _apollo: https://www.apollographql.com
.. _django-rest-framework-jwt: https://github.com/GetBlimp/django-rest-framework-jwt
.. _django-cors-headers-jwt: https://github.com/ottoyiu/django-cors-headers
.. _mutation: http://graphql.org/learn/queries/#mutations
