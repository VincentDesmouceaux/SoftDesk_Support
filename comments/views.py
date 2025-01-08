from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from .models import Comment
from .serializers import CommentSerializer
from authentication.permissions import IsAuthorOrAdminOrReadOnly, IsProjectContributor
from issues.models import Issue


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor, IsAuthorOrAdminOrReadOnly]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        issue_id = self.kwargs.get('issue_id')
        return Comment.objects.filter(issue_id=issue_id, issue__project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        issue_id = self.kwargs.get('issue_id')
        issue = get_object_or_404(Issue, id=issue_id, project_id=project_id)
        serializer.save(author=self.request.user, issue=issue)
