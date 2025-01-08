"""
Ce module contient les vues (ViewSets) relatives aux Projets (Project).
Il gère la logique d'API pour la création, la consultation, la modification
et la suppression des projets, ainsi que les permissions associées.
"""

from rest_framework import viewsets, permissions
from django.http import Http404
from .models import Project
from .serializers import ProjectSerializer
from authentication.permissions import IsAuthorOrAdminOrReadOnly


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet gérant les opérations CRUD sur le modèle Project.
    - list: Récupère tous les projets.
    - retrieve: Récupère un projet spécifique par son ID.
    - create: Crée un nouveau projet.
    - update/partial_update: Modifie un projet existant.
    - destroy: Supprime un projet.

    Les permissions exigent que l'utilisateur soit authentifié et
    respecte IsAuthorOrAdminOrReadOnly.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdminOrReadOnly]

    def get_queryset(self):
        """
        Retourne la liste des projets.
        Pour simplifier, ici on retourne tous les projets si l'utilisateur est superadmin.
        Sinon, on peut restreindre aux projets auxquels l'utilisateur est réellement attaché.

        Returns:
            QuerySet: Ensemble des projets pertinents pour l'utilisateur.
        """
        if self.request.user.is_superuser:
            return Project.objects.all()
        return Project.objects.all()

    def get_object(self):
        """
        Récupère un projet par son ID, sans filtrer par l'utilisateur,
        afin de différencier une erreur 404 (projet introuvable) d'une erreur 403 (accès refusé).

        Raises:
            Http404: Si le projet n'existe pas.

        Returns:
            Project: L'instance du projet demandée.
        """
        project_id = self.kwargs.get('pk')  # ou 'project_id' selon la route
        try:
            obj = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise Http404("Ce projet n'existe pas.")
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        """
        Surchage de la méthode de création afin d'assigner l'auteur du projet
        et de l'ajouter à la liste des contributeurs.

        Args:
            serializer (ProjectSerializer): Sérialiseur du projet.
        """
        project = serializer.save(author=self.request.user)
        project.contributors.add(self.request.user)
