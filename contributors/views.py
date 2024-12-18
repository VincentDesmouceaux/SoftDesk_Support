from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Contributor
from .serializers import ContributorSerializer
from projects.models import Project
from authentication.permissions import IsAuthorOrAdminOrReadOnly, IsProjectContributor


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor, IsAuthorOrAdminOrReadOnly]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        if project_id:
            return Contributor.objects.filter(project_id=project_id)
        return Contributor.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("\n[DEBUG] ContributorViewSet.create() -> serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        project = serializer.validated_data.get('project', None)
        if project and (project.author != self.request.user and not self.request.user.is_superuser):
            raise PermissionDenied("Vous n'êtes pas autorisé à ajouter des contributeurs à ce projet.")

        if Contributor.objects.filter(user=serializer.validated_data['user'], project=project).exists():
            raise PermissionDenied("Ce contributeur est déjà lié à ce projet.")
        serializer.save()
