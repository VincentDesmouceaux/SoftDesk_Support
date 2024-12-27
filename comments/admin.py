from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'author', 'issue', 'created_time')
    list_filter = ('author', 'issue')
    search_fields = ('description', 'author__username', 'issue__title')
    ordering = ('-created_time',)


admin.site.register(Comment, CommentAdmin)
