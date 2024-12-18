from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Issue
from .serializers import IssueSerializer
from authentication.permissions import IsAuthorOrAdminOrReadOnly, IsProjectContributor
from projects.models import Project
from contributors.models import Contributor


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor, IsAuthorOrAdminOrReadOnly]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Issue.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, id=project_id)

        assignee_id = self.request.data.get('assignee', None)
        assignee = None
        if assignee_id is not None:
            # Vérifier que l'utilisateur assignee est contributeur
            if not Contributor.objects.filter(project=project, user_id=assignee_id).exists():
                raise PermissionDenied("L'assignee doit être contributeur du projet.")
            assignee = assignee_id

        serializer.save(author=self.request.user, project=project, assignee_id=assignee)
