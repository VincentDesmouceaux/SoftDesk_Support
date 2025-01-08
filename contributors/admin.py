"""
Fichier d'administration Django pour l'application Contributors.
Permet la gestion de l'objet Contributor via l'interface d'administration.
"""

from django.contrib import admin
from .models import Contributor


class ContributorAdmin(admin.ModelAdmin):
    """
    Personnalise l'affichage du modèle Contributor dans Django admin.
    """
    list_display = ('id', 'user', 'project', 'role')
    list_filter = ('project', 'role')
    search_fields = ('user__username', 'project__title')


admin.site.register(Contributor, ContributorAdmin)
