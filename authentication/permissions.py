from rest_framework.permissions import BasePermission


class IsAdminUserOrReadOnly(BasePermission):
    """
    Permission permettant uniquement aux super utilisateurs ou à un utilisateur de modifier ses propres informations.
    """

    def has_permission(self, request, view):
        """
        Vérifie les permissions générales pour la vue.
        """
        print(f"Checking general permissions: User: {request.user}, Action: {view.action}")
        if view.action in ['list', 'create']:
            return True  # Par défaut, ces actions sont ouvertes selon leur permission explicite
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Limite les permissions des objets individuels.
        """
        print(f"Checking object permissions: User: {request.user.username}, Action: {view.action}, Target: {obj.username}")
        # Vérifiez si l'utilisateur est super utilisateur ou s'il modifie ses propres informations.
        if view.action in ['update', 'partial_update', 'destroy']:
            is_allowed = obj.id == request.user.id or request.user.is_superuser
            print(f"Permission allowed: {is_allowed}")
            return is_allowed
        return True
