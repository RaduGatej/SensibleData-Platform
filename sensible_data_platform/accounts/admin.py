from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from accounts.models import Cas

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class CasInline(admin.StackedInline):
    model = Cas
    can_delete = True
    verbose_name_plural = 'cas'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (CasInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
