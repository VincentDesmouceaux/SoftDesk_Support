from rest_framework.permissions import BasePermission, SAFE_METHODS
from projects.models import Project


class IsAuthorOrAdminOrReadOnly(BasePermission):
    """
    Permet (GET) en lecture à tous les utilisateurs qui y ont accès (déjà géré par d’autres checks)
    Permet en écriture seulement à l’auteur ou au superuser.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        # Écriture : doit être author
        return (obj.author == request.user)


class IsIssueAuthorOrAssigneeOrAdminOrReadOnly(BasePermission):
    """
    Permet en lecture à tous les contributeurs (déjà géré par IsProjectContributor).
    Permet en écriture si l'utilisateur est superuser, ou l’auteur de l’Issue, ou l’assignee de l’Issue.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        # Pour l’écriture : author ou assignee
        return (obj.author == request.user) or (obj.assignee == request.user)


class IsProjectContributor(BasePermission):
    """
    Vérifie que l'utilisateur est contributeur ou auteur du projet associé à la vue.
    On suppose que project_id est présent dans les kwargs de la vue.
    """

    def has_permission(self, request, view):
        # Autoriser les superutilisateurs
        if request.user.is_superuser:
            return True

        project_id = view.kwargs.get('project_id')
        if project_id:
            return Project.objects.filter(id=project_id, contributors=request.user).exists() or \
                Project.objects.filter(id=project_id, author=request.user).exists()
        # Si aucune project_id, on considère que c'est une route globale
        # (par ex. liste de projets)
        return True


class IsActiveUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)
