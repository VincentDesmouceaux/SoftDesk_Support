from rest_framework.permissions import BasePermission, SAFE_METHODS
from projects.models import Project


class IsAuthorOrAdminOrReadOnly(BasePermission):
    """
    Permission :
    - Un superutilisateur (admin) a tous les droits (lecture & écriture).
    - Un utilisateur non admin peut lire (si déjà filtré par le fait d'être contributeur, ou autre)
      mais ne peut modifier une ressource que s'il en est l'auteur.
    """

    """
    - Lecture autorisée à tout utilisateur qui a accès au projet (déjà vérifié par IsProjectContributor).
    - Écriture autorisée si l'utilisateur est superuser, ou l'auteur de l'issue, ou l'assignee de l'issue.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # Méthodes de lecture autorisées
        if request.method in SAFE_METHODS:
            return True

        # Méthodes d'écriture : auteur OU assignee
        return (obj.author == request.user) or (obj.assignee == request.user)


class IsIssueAuthorOrAssigneeOrAdminOrReadOnly(BasePermission):
    """
    - Lecture autorisée à tout utilisateur qui a accès au projet (déjà vérifié par IsProjectContributor).
    - Écriture autorisée si l'utilisateur est superuser, ou l'auteur de l'issue, ou l'assignee de l'issue.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # Méthodes de lecture autorisées
        if request.method in SAFE_METHODS:
            return True

        # Méthodes d'écriture : auteur OU assignee
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
