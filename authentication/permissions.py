from rest_framework.permissions import BasePermission


class IsAdminUserOrReadOnly(BasePermission):
    """
    Permission permettant uniquement aux super utilisateurs d'accéder à la liste complète.
    """

    def has_permission(self, request, view):
        print(f"User: {request.user}, Is Superuser: {request.user.is_superuser}")
        if view.action == 'list':
            return request.user and request.user.is_superuser
        return True
