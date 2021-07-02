from django.contrib import admin
from authy.models import Profile
from authy.models import Report_Issue
admin.site.register(Report_Issue)
# Register your models here.

admin.site.register(Profile)