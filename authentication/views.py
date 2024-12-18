from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied
from .models import CustomUser
from .serializers import UserSerializer
from .permissions import IsAuthorOrAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        action = self.action
        user = self.request.user
        print(f"Action: {action} - User: {user}")
        if action == 'create':
            return [AllowAny()]
        elif action == 'list':
            return [IsAuthenticated(), IsAuthorOrAdminOrReadOnly()]
        return [IsAuthenticated(), IsAuthorOrAdminOrReadOnly()]

    def get_queryset(self):
        user = self.request.user
        print(f"Fetching queryset for user: {user.username}, Is Superuser: {user.is_superuser}")
        return CustomUser.objects.all()

    def check_permissions_for_update(self, user, instance):
        if user.is_superuser:
            return
        is_allowed = instance.id == user.id
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
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrAdminOrReadOnly]

    def get_object(self):
        user = self.request.user
        print(f"Fetching profile for user: {user.username}")
        return user
