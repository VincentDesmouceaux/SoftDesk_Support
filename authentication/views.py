from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, generics, status
from .models import CustomUser
from .serializers import UserSerializer
from .permissions import IsAuthorOrAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    Vue pour gérer les utilisateurs (CRUD).
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        action = self.action
        user = self.request.user
        print(f"Action: {action} - User: {user}")

        if action == 'create':
            # Création accessible à tous
            return [AllowAny()]
        elif action == 'list':
            # Liste accessible seulement aux utilisateurs authentifiés
            return [IsAuthenticated()]
        else:
            # retrieve, update, partial_update, destroy => authentifié
            return [IsAuthenticated()]

    def check_permissions_for_update(self, user, instance):
        # Si superadmin => OK
        if user.is_superuser:
            return
        # Sinon, autorisé uniquement si c’est lui-même
        is_allowed = (instance.id == user.id)
        print(f"Permission check for update: User: {user.username}, Target: {instance.username}, Allowed: {is_allowed}")
        if not is_allowed:
            raise PermissionDenied("Vous ne pouvez modifier que vos propres informations.")

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(f"Partial update attempt by: {request.user.username} on {instance.username}")
        self.check_permissions_for_update(request.user, instance)
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(f"Update attempt by: {request.user.username} on {instance.username}")
        self.check_permissions_for_update(request.user, instance)
        return super().update(request, *args, **kwargs)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Vue pour récupérer et mettre à jour le profil de l'utilisateur connecté.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrAdminOrReadOnly]

    def get_object(self):
        user = self.request.user
        print(f"Fetching profile for user: {user.username}")
        return user


class SecureEndpoint(APIView):
    """
    Vue sécurisée pour tester les accès via JWT.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": f"Bienvenue {request.user.username}, vous êtes authentifié(e) avec succès !"
        })
