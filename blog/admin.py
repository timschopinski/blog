from django.contrib import admin
from . models import Post, Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "author")
    list_filter = ("author",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name",)
    list_filter = ("user_name",)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)