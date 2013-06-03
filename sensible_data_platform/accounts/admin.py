from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from accounts.models import Cas
from accounts.models import Participant

class CasInline(admin.StackedInline):
    model = Cas
    can_delete = True
    verbose_name_plural = 'cas'


class UserAdmin(UserAdmin):
    inlines = (CasInline, )


class ParticipantInline(admin.StackedInline):
    model = Participant
    can_delete = True
    verbose_name_plural = 'participant'

class UserAdmin(UserAdmin):
	inlines = (ParticipantInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
