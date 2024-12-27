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

# Configuration du schéma Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="SoftDesk API",
        default_version="v1",
        description="Documentation de l'API SoftDesk",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

# Configuration des routes principales avec un router DRF
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profil utilisateur
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),

    # Endpoint sécurisé pour tester l'authentification
    path('api/secure-endpoint/', SecureEndpoint.as_view(), name='secure-endpoint'),

    # Routes du router principal
    path('api/', include(router.urls)),

    # Route nestée pour contributors
    path('api/projects/<uuid:project_id>/contributors/',
         ContributorViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='project-contributors'),

    path('api/projects/<uuid:project_id>/contributors/<int:pk>/',
         ContributorViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='project-contributor-detail'),

    # Routes nestées pour issues
    path('api/projects/<uuid:project_id>/issues/',
         IssueViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='project-issues'),

    path('api/projects/<uuid:project_id>/issues/<uuid:pk>/',
         IssueViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='project-issue-detail'),

    # Routes nestées pour comments
    path('api/projects/<uuid:project_id>/issues/<uuid:issue_id>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='issue-comments'),

    path('api/projects/<uuid:project_id>/issues/<uuid:issue_id>/comments/<uuid:pk>/',
         CommentViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='issue-comment-detail'),

    # Documentation Swagger
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
]
