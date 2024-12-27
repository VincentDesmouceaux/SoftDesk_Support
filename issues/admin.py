from django.contrib import admin
from .models import Issue


class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'tag', 'priority', 'status', 'project', 'author', 'created_time')
    list_filter = ('tag', 'priority', 'status', 'project', 'author')
    search_fields = ('title', 'description', 'author__username', 'project__title')
    ordering = ('-created_time',)


admin.site.register(Issue, IssueAdmin)
