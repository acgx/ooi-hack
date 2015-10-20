from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import ONode, OTopic

admin.site.register(ONode, MPTTModelAdmin)
admin.site.register(OTopic)
