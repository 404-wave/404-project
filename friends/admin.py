from django.contrib import admin

from .models import *


class FollowAdmin(admin.ModelAdmin):
    search_fields = ['user1_id', 'user2_id']
    list_display = ['user1_id', 'user2_id']


admin.site.register(Follow, FollowAdmin)
admin.site.register(FriendRequest)
