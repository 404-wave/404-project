from django.contrib import admin

from .models import *


class FollowAdmin(admin.ModelAdmin):
    search_fields = ['user1', 'user2']
    list_display = ['user1', 'user2']


admin.site.register(Follow, FollowAdmin)
admin.site.register(FriendRequest)
