from django.contrib import admin

# Register your models here.
from .models import Post

# NOTE: It IS possible to have links in the admin interface, so later on we
# will be able to have anchor tag links to images related to posts.

# https://docs.djangoproject.com/en/2.1/ref/contrib/admin/


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "timestamp", "updated"]
    list_display_links = ["id", "user", "updated"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["content", "user__username"]

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)
