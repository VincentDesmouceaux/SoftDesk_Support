from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Project
from .serializers import ProjectSerializer
from authentication.permissions import IsAuthorOrAdminOrReadOnly


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Project.objects.all()
        return Project.objects.filter(Q(author=user) | Q(contributors=user)).distinct()

    def perform_create(self, serializer):
        # L'utilisateur qui "souscrit" devient l'auteur du projet
        project = serializer.save(author=self.request.user)
        # Ajout automatique de l'auteur comme contributeur du projet
        project.contributors.add(self.request.user)
