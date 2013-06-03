from oauth2app.models import *
from django.contrib import admin

class AccessRangeAdmin(admin.ModelAdmin):
	list_display = ('key', 'description')
	class Meta:
		verbose_name = 'scope'


admin.site.register(AccessRange, AccessRangeAdmin)

class ClientAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'user', 'api_uri')
	def get_readonly_fields(self, request, obj=None):
		if obj is not None:
			return self.readonly_fields + ('user',)
		return self.readonly_fields

admin.site.register(Client, ClientAdmin)

class AccessTokenAdmin(admin.ModelAdmin):
	list_display = ('user', 'token')

admin.site.register(AccessToken, AccessTokenAdmin)
