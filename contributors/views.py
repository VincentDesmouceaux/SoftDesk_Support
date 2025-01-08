"""
Ce module contient le ViewSet pour gérer les contributeurs (Contributor) d'un projet,
ainsi que les règles de permissions liées à la création, la suppression, etc.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Contributor
from .serializers import ContributorSerializer
from authentication.permissions import IsAuthorOrAdminOrReadOnly, IsProjectContributor


class ContributorViewSet(viewsets.ModelViewSet):
    """
    ViewSet gérant les opérations CRUD (list, retrieve, create, partial_update, destroy)
    pour les contributeurs d'un projet.

    Permissions:
        - L'utilisateur doit être authentifié et contributeur (IsProjectContributor)
        - Seul l'auteur du projet, un superuser ou le contributeur lui-même peut supprimer.
        - Pour créer un nouveau contributor, seule l'authentification est requise.
    """
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor, IsAuthorOrAdminOrReadOnly]

    def get_queryset(self):
        """
        Renvoie la liste des contributeurs d'un projet donné par project_id dans l'URL.
        Si aucun project_id n'est fourni, renvoie un queryset vide.
        """
        project_id = self.kwargs.get('project_id')
        if project_id:
            return Contributor.objects.filter(project_id=project_id)
        return Contributor.objects.none()

    def create(self, request, *args, **kwargs):
        """
        Crée un nouveau contributor.
        Si le sérialiseur n'est pas valide, renvoie une 400 avec les erreurs.
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("\n[DEBUG] ContributorViewSet.create() -> serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Vérifie qu'un contributeur identique n'existe pas déjà avant de créer un nouveau Contributor.

        Raises:
            PermissionDenied: si un contributeur identique (même user et même projet) existe déjà.
        """
        project = serializer.validated_data.get('project', None)
        if Contributor.objects.filter(
            user=serializer.validated_data['user'],
            project=project
        ).exists():
            raise PermissionDenied("Cet utilisateur est déjà contributeur de ce projet.")

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        Supprime un contributor.
        Seul le superuser, l'auteur du projet ou l'utilisateur lui-même peut effectuer cette suppression.
        Sinon, renvoie une 403.
        """
        contributor_instance = self.get_object()
        if (
            request.user.is_superuser
            or request.user == contributor_instance.user
            or request.user == contributor_instance.project.author
        ):
            return super().destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied("Vous ne pouvez pas supprimer ce contributeur.")

    def get_permissions(self):
        """
        Définit dynamiquement les permissions selon l'action en cours.
        - create: Seulement IsAuthenticated
        - autre: IsAuthenticated + IsProjectContributor + IsAuthorOrAdminOrReadOnly
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [
                permissions.IsAuthenticated,
                IsProjectContributor,
                IsAuthorOrAdminOrReadOnly,
            ]
        return [permission() for permission in permission_classes]
