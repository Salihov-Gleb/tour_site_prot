from django.contrib import admin
from main_app.models import Post, Comment, Photos


class PostAdmin(admin.ModelAdmin):
    exclude = []


class CommentAdmin(admin.ModelAdmin):
    exclude = []


class PhotosAdmin(admin.ModelAdmin):
    exclude = []


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Photos, PhotosAdmin)
