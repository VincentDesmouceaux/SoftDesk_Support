from django.contrib import admin
from .models import Contributor


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'role')
    list_filter = ('project', 'role')
    search_fields = ('user__username', 'project__title')


admin.site.register(Contributor, ContributorAdmin)
