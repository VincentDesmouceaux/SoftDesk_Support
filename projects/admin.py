from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'project_type', 'author', 'created_time')
    list_filter = ('project_type', 'author')
    search_fields = ('title', 'description', 'author__username')
    ordering = ('-created_time',)


admin.site.register(Project, ProjectAdmin)
