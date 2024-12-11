from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]  # Permet la création d'un utilisateur sans authentification
        elif self.action == 'list':
            if self.request.user.is_superuser:
                return [IsAuthenticated()]  # Seuls les super utilisateurs peuvent voir la liste
            else:
                self.permission_denied(
                    self.request,
                    message="Seuls les administrateurs peuvent accéder à cette ressource."
                )
        return [IsAuthenticated()]  # Les autres actions nécessitent une authentification

    def perform_create(self, serializer):
        age = serializer.validated_data.get('age')
        if age and age < 15:
            raise ValidationError("L'utilisateur doit avoir au moins 15 ans pour s'inscrire.")
        serializer.save()
