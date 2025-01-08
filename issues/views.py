"""
Ce module contient le ViewSet pour les Issues, gérant la logique d'API liée
aux tickets (Issues) dans un projet. Les permissions sont vérifiées pour
assurer que seuls les contributeurs ou administrateurs puissent modifier/voir.
"""

from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Issue
from .serializers import IssueSerializer
from authentication.permissions import IsIssueAuthorOrAssigneeOrAdminOrReadOnly, IsProjectContributor
from projects.models import Project
from contributors.models import Contributor


class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet gérant les opérations CRUD sur le modèle Issue.
    - list: liste des issues d'un projet
    - retrieve: détails d'une issue
    - create: création d'une issue
    - update/partial_update: modification d'une issue
    - destroy: suppression d'une issue

    Permissions :
        - IsAuthenticated
        - IsProjectContributor
        - IsIssueAuthorOrAssigneeOrAdminOrReadOnly
    """
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor, IsIssueAuthorOrAssigneeOrAdminOrReadOnly]

    def get_queryset(self):
        """
        Retourne le queryset d'issues filtrées par l'ID du projet passé dans l'URL.

        Returns:
            QuerySet: Les issues liées au projet.
        """
        project_id = self.kwargs.get('project_id')
        return Issue.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        """
        Méthode appelée lors de la création d'une issue.
        Vérifie que l'assignee (si fourni) est bien contributeur du projet
        avant d'enregistrer l'issue.

        Args:
            serializer (IssueSerializer): Sérialiseur de l'issue.

        Raises:
            PermissionDenied: Si l'utilisateur assigné n'est pas contributeur.
        """
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, id=project_id)

        assignee_id = self.request.data.get('assignee', None)
        assignee = None
        if assignee_id is not None:
            # Vérifier que l'utilisateur assigné est contributeur du projet
            if not Contributor.objects.filter(project=project, user_id=assignee_id).exists():
                raise PermissionDenied("L'assignee doit être contributeur du projet.")
            assignee = assignee_id

        serializer.save(author=self.request.user, project=project, assignee_id=assignee)
