from django.contrib import admin
from .models import Category, Tag, Post, Newsletter
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
class PostAdmin(SummernoteModelAdmin):
    list_display = ("title", "author", "category", "status", "created_at", "updated_at")
    list_filter = ("status", "category", "tags")
    search_fields = ("title", "content")
    summernote_fields = ("content",)


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Newsletter)
