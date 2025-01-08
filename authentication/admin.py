"""
Configuration de l'interface d'administration Django pour le modèle CustomUser.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Personnalisation de l'affichage du CustomUser dans Django admin.
    """
    list_display = ('username', 'email', 'is_staff', 'is_active', 'age', 'can_be_contacted', 'can_data_be_shared')
    list_filter = ('is_staff', 'is_active', 'can_be_contacted', 'can_data_be_shared')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('email', 'age', 'can_be_contacted', 'can_data_be_shared')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'age', 'is_staff', 'is_active'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
