from django.contrib import admin

from .models import OUser, OUserEmailVerification, OUserPasswordReset


class OUseAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email']

admin.site.register(OUser, OUseAdmin)
admin.site.register(OUserEmailVerification)
admin.site.register(OUserPasswordReset)
