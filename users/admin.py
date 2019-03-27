from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):

    search_fields = ['username', 'first_name', 'last_name']
    list_display = ['id', 'username', 'first_name', 'last_name']
    list_filter = ('is_active', 'is_superuser')
    ordering = ('-date_joined',)


class NodeAdmin(admin.ModelAdmin):

    search_fields = ['host']
    list_display = ['id', 'host', 'sharing']
    list_filter = ('sharing',)


class NodeSettingAdmin(admin.ModelAdmin):

    list_display = ['id']


admin.site.register(User, UserAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(NodeSetting, NodeSettingAdmin)
