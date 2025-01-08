"""
Vues (ViewSets et APIViews) gérant l'authentification et la gestion des utilisateurs.
Inclut la création et la mise à jour d'utilisateurs, leur profil, etc.
"""

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, generics
from .models import CustomUser
from .serializers import UserSerializer
from .permissions import IsAuthorOrAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet permettant de gérer le CRUD des utilisateurs (CustomUser).
    - create (POST) accessible à tous
    - list, retrieve, update, partial_update, destroy accessibles uniquement aux utilisateurs authentifiés
    - Un utilisateur ne peut modifier ou supprimer que son propre compte, sauf si c'est un superuser.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Détermine dynamiquement les permissions en fonction de l'action.
        """
        action = self.action
        user = self.request.user
        print(f"Action: {action} - User: {user}")

        if action == 'create':
            return [AllowAny()]
        elif action == 'list':
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated()]

    def check_permissions_for_update(self, user, instance):
        """
        Vérifie si l'utilisateur dispose des droits pour mettre à jour l'instance cible.
        - Un superuser peut tout modifier
        - Sinon l'utilisateur ne peut modifier que son propre compte
        """
        if user.is_superuser:
            return
        is_allowed = (instance.id == user.id)
        print(f"Permission check for update: User: {user.username}, Target: {instance.username}, Allowed: {is_allowed}")
        if not is_allowed:
            raise PermissionDenied("Vous ne pouvez modifier que vos propres informations.")

    def partial_update(self, request, *args, **kwargs):
        """
        Surcharge pour vérifier les permissions avant la mise à jour partielle.
        """
        instance = self.get_object()
        print(f"Partial update attempt by: {request.user.username} on {instance.username}")
        self.check_permissions_for_update(request.user, instance)
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Surcharge pour vérifier les permissions avant la mise à jour complète.
        """
        instance = self.get_object()
        print(f"Update attempt by: {request.user.username} on {instance.username}")
        self.check_permissions_for_update(request.user, instance)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Un utilisateur ne peut détruire que son propre compte, sauf si c'est un superuser.
        """
        instance = self.get_object()
        if not (request.user.is_superuser or request.user == instance):
            raise PermissionDenied("Vous ne pouvez pas supprimer un autre utilisateur.")
        return super().destroy(request, *args, **kwargs)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Vue pour récupérer et mettre à jour le profil de l'utilisateur connecté.
    Accessible uniquement à l'utilisateur authentifié lui-même (ou un admin).
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrAdminOrReadOnly]

    def get_object(self):
        """
        Renvoie l'utilisateur actuellement authentifié comme objet-cible.
        """
        user = self.request.user
        print(f"Fetching profile for user: {user.username}")
        return user


class SecureEndpoint(APIView):
    """
    Vue simple et sécurisée pour tester l'authentification JWT.
    Renvoie un message de bienvenue si l'utilisateur est correctement authentifié.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Renvoie un message confirmant l'authentification de l'utilisateur.
        """
        return Response({
            "message": f"Bienvenue {request.user.username}, vous êtes authentifié(e) avec succès !"
        })
