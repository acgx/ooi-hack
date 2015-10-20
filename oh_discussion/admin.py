from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import ONode, OTopic, OReply

admin.site.register(ONode, MPTTModelAdmin)
admin.site.register(OTopic)
admin.site.register(OReply)
