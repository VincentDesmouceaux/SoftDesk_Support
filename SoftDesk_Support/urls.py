from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import UserViewSet, UserProfileView  # Importer les vues correctement

# Définir les routes avec le router DRF
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')  # Gestion des utilisateurs (CRUD)

# Ajouter toutes les URLs dans urlpatterns
urlpatterns = [
    # Interface d'administration
    path('admin/', admin.site.urls),

    # Routes liées à l'authentification (JWT)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Route pour accéder au profil utilisateur connecté
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),

    # Inclusion des routes définies par le router
    path('api/', include(router.urls)),
]
