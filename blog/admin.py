from django.contrib import admin
from .models import Category, Tag, Post


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "created_at", "updated_at")
    list_filter = ("status", "category", "tags")
    search_fields = ("title", "content")


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
