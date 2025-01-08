"""
Ce module contient le ViewSet pour gérer les commentaires (Comment) liés à une issue.
Les permissions sont gérées de façon à ce que seuls les contributeurs puissent
créer ou modifier un commentaire sur l'issue.
"""

from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from .models import Comment
from .serializers import CommentSerializer
from authentication.permissions import IsAuthorOrAdminOrReadOnly, IsProjectContributor
from issues.models import Issue


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet gérant les opérations CRUD pour les commentaires :
    - list: Liste de tous les commentaires d'une issue
    - retrieve: Récupère un commentaire en particulier
    - create: Ajoute un commentaire
    - update/partial_update: Modifie un commentaire
    - destroy: Supprime un commentaire

    Permissions:
        - IsAuthenticated
        - IsProjectContributor
        - IsAuthorOrAdminOrReadOnly (l'auteur du commentaire ou admin peut le modifier/supprimer)
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor, IsAuthorOrAdminOrReadOnly]

    def get_queryset(self):
        """
        Récupère les commentaires liés à l'issue en se basant sur l'ID du projet et de l'issue.

        Returns:
            QuerySet: Tous les commentaires liés à l'issue spécifiée.
        """
        project_id = self.kwargs.get('project_id')
        issue_id = self.kwargs.get('issue_id')
        return Comment.objects.filter(issue_id=issue_id, issue__project_id=project_id)

    def perform_create(self, serializer):
        """
        Associe le commentaire à l'issue correspondante et définit l'auteur
        comme l'utilisateur actuellement authentifié.

        Args:
            serializer (CommentSerializer): Sérialiseur du commentaire.
        """
        project_id = self.kwargs.get('project_id')
        issue_id = self.kwargs.get('issue_id')
        issue = get_object_or_404(Issue, id=issue_id, project_id=project_id)
        serializer.save(author=self.request.user, issue=issue)
