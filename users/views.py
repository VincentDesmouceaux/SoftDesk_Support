from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from .models import CustomUser
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        age = serializer.validated_data.get('age')
        if age < 15:
            raise ValidationError("L'utilisateur doit avoir au moins 15 ans pour s'inscrire.")
        serializer.save()
