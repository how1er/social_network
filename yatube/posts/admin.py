from queue import Empty
from re import search
from django.contrib import admin

# Register your models here.

from .models import Post, Group, Comment,Follow

class PostAdmin(admin.ModelAdmin):
    list_display = ("pk","text", "pub_date", "author")
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "- пусто -"

class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug", "description" )
    empty_value_display = "- пусто -"

class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "created", "author", "post" )
    empty_value_display = "- пусто -"



admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow)