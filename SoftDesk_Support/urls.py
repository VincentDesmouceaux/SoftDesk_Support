from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import UserViewSet, UserProfileView
from projects.views import ProjectViewSet
from contributors.views import ContributorViewSet
from rest_framework.routers import DefaultRouter

# Router principal
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
# CHANGEMENT: On ne déclare plus 'contributors' ici, on utilise une URL nestée plus bas.

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profil utilisateur
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),

    # Routes du router principal
    path('api/', include(router.urls)),

    # CHANGEMENT: Route nestée pour contributors
    path('api/projects/<uuid:project_id>/contributors/',
         ContributorViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='project-contributors'),
]
