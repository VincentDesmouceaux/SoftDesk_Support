from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, generics
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
        if self.action == 'create':
            return [AllowAny()]  # Permet la création sans authentification
        elif self.action == 'list':
            return [IsAdminUserOrReadOnly()]  # Restreint l'accès complet aux super utilisateurs
        return [IsAuthenticated()]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Vue pour permettre à un utilisateur connecté de voir ou modifier son profil.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
