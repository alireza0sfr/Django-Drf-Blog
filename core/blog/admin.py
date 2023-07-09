from django.contrib import admin

from .models import Post, Category


class CustomPostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('id', 'author', 'title', 'content', 'status', 'category', 'image', 'created_date')
    list_filter = list_display
    search_fields = list_display
    ordering = list_display


class CustomCategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('id', 'name', 'created_date')
    list_filter = list_display
    search_fields = list_display
    ordering = list_display


admin.site.register(Post, CustomPostAdmin)
admin.site.register(Category, CustomCategoryAdmin)
