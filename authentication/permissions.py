"""
Module de permissions personnalisées, gérant des règles supplémentaires
concernant l'accès aux ressources.
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS
from projects.models import Project


class IsAuthorOrAdminOrReadOnly(BasePermission):
    """
    Autorise la lecture à tous les utilisateurs (ayant déjà accès par ailleurs),
    et l'écriture seulement à l'auteur de l'objet ou un superuser.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        return (obj.author == request.user)


class IsIssueAuthorOrAssigneeOrAdminOrReadOnly(BasePermission):
    """
    Autorise la lecture à tous les contributeurs (géré par IsProjectContributor).
    Autorise l'écriture uniquement à l'auteur de l'issue, à l'assignee ou au superuser.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        return (obj.author == request.user) or (obj.assignee == request.user)


class IsProjectContributor(BasePermission):
    """
    Vérifie que l'utilisateur est contributeur ou auteur du projet associé à la vue.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        project_id = view.kwargs.get('project_id')
        if project_id:
            return (
                Project.objects.filter(id=project_id, contributors=request.user).exists()
                or Project.objects.filter(id=project_id, author=request.user).exists()
            )
        return True


class IsActiveUser(BasePermission):
    """
    Vérifie que l'utilisateur est actif (non banni ou désactivé).
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)
