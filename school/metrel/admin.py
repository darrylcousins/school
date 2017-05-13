__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

from django.contrib import admin

from .models import Results
from .models import Limits
from .models import Functions
from .models import Appliances
from .models import AutoTests
from .models import Users
from .models import Projects
from .models import Premises
from .models import BusinessSubjects


admin.site.register(Results)
admin.site.register(Limits)
admin.site.register(Functions)
admin.site.register(Appliances)
admin.site.register(AutoTests)
admin.site.register(Users)
admin.site.register(Projects)
admin.site.register(Premises)
admin.site.register(BusinessSubjects)

