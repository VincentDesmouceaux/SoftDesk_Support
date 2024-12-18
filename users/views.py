from rest_framework import generics
from authentication.models import CustomUser
from authentication.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Vue pour permettre à un utilisateur connecté de voir ou modifier son profil.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
