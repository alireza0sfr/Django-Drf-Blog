from django.contrib import admin

from comment.models import Comment


class CustomCommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('id', 'author', 'content', 'created_date')
    list_filter = list_display
    search_fields = list_display
    ordering = list_display


admin.site.register(Comment, CustomCommentAdmin)