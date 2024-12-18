from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Configuration des champs affichés dans la liste
    list_display = ('username', 'email', 'is_staff', 'is_active', 'age', 'can_be_contacted', 'can_data_be_shared')
    list_filter = ('is_staff', 'is_active', 'can_be_contacted', 'can_data_be_shared')
    ordering = ('username',)

    # Configuration des champs affichés dans les formulaires de création/modification
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('email', 'age', 'can_be_contacted', 'can_data_be_shared')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Champs pour le formulaire de création
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'age', 'is_staff', 'is_active'),
        }),
    )


# Enregistrement du modèle dans l'interface admin
admin.site.register(CustomUser, CustomUserAdmin)
