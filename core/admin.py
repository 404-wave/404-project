from django.contrib import admin

# from .models import Post, Comment


# NOTE: It IS possible to have links in the admin interface, so later on we
# will be able to have anchor tag links to images related to posts.

# class PostAdmin(admin.ModelAdmin):

#     search_fields = ['id', 'user_id', 'date']
#     list_display = ['id', 'user_id', 'date']
#     list_filter = ('privacy', 'unlisted')
#     ordering = ('user_id', '-date',)


# class CommentAdmin(admin.ModelAdmin):

#     search_fields = ['post_id']
#     list_display = ['post_id', 'date']
#     ordering = ('-date',)


# admin.site.register(Post, PostAdmin)
# admin.site.register(Comment, CommentAdmin)
