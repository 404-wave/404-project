from django.contrib import admin

from .models import Post


# https://docs.djangoproject.com/en/2.1/ref/contrib/admin/
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "timestamp", "updated"]
    list_display_links = ["id", "user", "timestamp", "updated"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["content", "user__username"]

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)
