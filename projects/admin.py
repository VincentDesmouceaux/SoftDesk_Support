"""
Fichier d'administration Django pour l'application Projects.
Permet la gestion de l'objet Project via l'interface d'administration.
"""

from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    """
    Classe d'administration pour personnaliser l'affichage du modèle Project dans l'admin Django.
    """
    list_display = ('id', 'title', 'project_type', 'author', 'created_time')
    list_filter = ('project_type', 'author')
    search_fields = ('title', 'description', 'author__username')
    ordering = ('-created_time',)


admin.site.register(Project, ProjectAdmin)
