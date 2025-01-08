from rest_framework import viewsets, permissions
from .models import Project
from .serializers import ProjectSerializer
from authentication.permissions import IsAuthorOrAdminOrReadOnly
from django.http import Http404


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdminOrReadOnly]

    def get_queryset(self):
        """
        On décide ici de retourner tous les projets si le besoin métier le justifie
        (ou éventuellement seulement ceux auxquels l'utilisateur a accès).
        """
        if self.request.user.is_superuser:
            return Project.objects.all()
        # ========================================
        # Selon le besoin :
        # Si on veut que "tout utilisateur connecté" voie TOUS les projets => on met:
        return Project.objects.all()

        # OU si on veut seulement les projets auxquels l'user a accès (comme avant) => on met:
        # return Project.objects.filter(
        #     Q(author=self.request.user) | Q(contributors=self.request.user)
        # ).distinct()

    def get_object(self):
        """
        Récupère l'objet (projet) indépendamment du queryset filtré
        afin de distinguer "pas trouvé" (vrai 404) et 
        "pas autorisé à y accéder" (403).
        """
        project_id = self.kwargs.get('pk')  # ou 'project_id' selon la route
        # On essaie de récupérer le projet *vraiment*, sans le filtrage du queryset
        try:
            obj = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            # Si le projet n'existe pas du tout dans la base
            raise Http404("Ce projet n'existe pas.")

        # Maintenant on vérifie les permissions d'accès
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        project.contributors.add(self.request.user)
