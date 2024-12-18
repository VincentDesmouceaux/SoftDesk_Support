from rest_framework.permissions import BasePermission, SAFE_METHODS
from projects.models import Project


class IsAuthorOrAdminOrReadOnly(BasePermission):
    """
    Permission :
    - Un superutilisateur (admin) a tous les droits.
    - Un utilisateur non admin peut lire (si déjà filtré par le fait d'être contributeur)
      mais ne peut modifier une ressource que s'il en est l'auteur.
    """

    def has_object_permission(self, request, view, obj):
        # Si l'utilisateur est superutilisateur : accès total
        if request.user.is_superuser:
            return True

        # Méthodes de lecture autorisées
        if request.method in SAFE_METHODS:
            return True

        # Méthodes d'écriture (POST, PUT, PATCH, DELETE) : doit être l'auteur
        return getattr(obj, 'author', None) == request.user


class IsProjectContributor(BasePermission):
    """
    Vérifie que l'utilisateur est contributeur ou auteur du projet associé à la vue.
    On suppose que project_id est présent dans les kwargs de la vue.
    """

    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_id')
        if project_id is not None:
            return Project.objects.filter(id=project_id, contributors=request.user).exists() or \
                Project.objects.filter(id=project_id, author=request.user).exists()
        # Si aucune project_id, on considère que c'est une route globale
        # (par ex. liste de projets, gérée par d'autres permissions ou filtres)
        return True
