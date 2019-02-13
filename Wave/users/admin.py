from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):

    search_fields = ['username', 'first_name', 'last_name']
    list_display = ['id', 'username', 'first_name', 'last_name']
    list_filter = ('is_active', 'is_superuser')
    ordering = ('-date_joined',)

admin.site.register(User, UserAdmin)
