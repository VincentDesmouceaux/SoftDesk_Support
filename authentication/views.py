from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied
from .models import CustomUser
from .serializers import UserSerializer
from .permissions import IsAdminUserOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les utilisateurs (CRUD).
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Définit les permissions en fonction de l'action.
        """
        action = self.action
        user = self.request.user
        print(f"Action: {action} - User: {user}")
        if action == 'create':
            return [AllowAny()]  # Création accessible sans authentification
        elif action == 'list':
            return [IsAdminUserOrReadOnly()]  # Listage réservé aux super utilisateurs
        return [IsAuthenticated()]  # Authentification nécessaire pour les autres actions

    def get_queryset(self):
        user = self.request.user
        print(f"Fetching queryset for user: {user.username}, Is Superuser: {user.is_superuser}")
        # Ne filtrez plus par utilisateur ici, renvoyez tous les utilisateurs
        return CustomUser.objects.all()

    def check_permissions_for_update(self, user, instance):
        """
        Vérifie si l'utilisateur peut modifier les données de l'instance.
        """
        is_allowed = instance.id == user.id or user.is_superuser
        print(f"Permission check for update: User: {user.username}, Target: {instance.username}, Allowed: {is_allowed}")
        if not is_allowed:
            raise PermissionDenied("Vous ne pouvez modifier que vos propres informations.")  # Permission refusée

    def partial_update(self, request, *args, **kwargs):
        """
        Gestion des mises à jour partielles.
        """
        instance = self.get_object()
        print(f"Partial update attempt by: {request.user.username} on {instance.username}")
        self.check_permissions_for_update(request.user, instance)  # Validation des permissions
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Gestion des mises à jour complètes.
        """
        instance = self.get_object()
        print(f"Update attempt by: {request.user.username} on {instance.username}")
        self.check_permissions_for_update(request.user, instance)  # Validation des permissions
        return super().update(request, *args, **kwargs)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Vue pour permettre à un utilisateur connecté de voir ou modifier son profil.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retourne l'utilisateur connecté.
        """
        user = self.request.user
        print(f"Fetching profile for user: {user.username}")
        return user
