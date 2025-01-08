"""
Fichier de configuration des URL principales du projet SoftDesk_Support.
Il gère l'association entre les URL et les vues (ou ViewSets) de l'application.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import UserViewSet, UserProfileView, SecureEndpoint
from projects.views import ProjectViewSet
from contributors.views import ContributorViewSet
from issues.views import IssueViewSet
from comments.views import CommentViewSet
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

# Configuration du schéma Swagger pour la documentation interactive
schema_view = get_schema_view(
    openapi.Info(
        title="SoftDesk API",
        default_version="v1",
        description="Documentation de l'API SoftDesk",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

# Configuration du router principal pour regrouper certaines vues de type ViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    # Accès à l'administration Django
    path('admin/', admin.site.urls),

    # Endpoints d'authentification avec JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Vue pour consulter et mettre à jour le profil de l'utilisateur connecté
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),

    # Endpoint sécurisé pour tester l'authentification
    path('api/secure-endpoint/', SecureEndpoint.as_view(), name='secure-endpoint'),

    # Inclusion des routes gérées par le router principal
    path('api/', include(router.urls)),

    # Routes nestées pour les Contributors
    path('api/projects/<uuid:project_id>/contributors/',
         ContributorViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='project-contributors'),
    path('api/projects/<uuid:project_id>/contributors/<int:pk>/',
         ContributorViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='project-contributor-detail'),

    # Routes nestées pour les Issues
    path('api/projects/<uuid:project_id>/issues/',
         IssueViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='project-issues'),
    path('api/projects/<uuid:project_id>/issues/<uuid:pk>/',
         IssueViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='project-issue-detail'),

    # Routes nestées pour les Comments
    path('api/projects/<uuid:project_id>/issues/<uuid:issue_id>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='issue-comments'),
    path('api/projects/<uuid:project_id>/issues/<uuid:issue_id>/comments/<uuid:pk>/',
         CommentViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='issue-comment-detail'),

    # Documentation Swagger
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
]
