from django.contrib import admin
from .models import Profile, Message, Tg_response_msg


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'created_at')

class Tg_response_msgAdmin(admin.ModelAdmin):
    list_display = ('id', 'command', 'content')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Tg_response_msg, Tg_response_msgAdmin)

