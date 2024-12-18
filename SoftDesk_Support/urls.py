from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import UserViewSet, UserProfileView
from projects.views import ProjectViewSet
from contributors.views import ContributorViewSet
from issues.views import IssueViewSet
from comments.views import CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
# Pas de contributor direct, déjà géré par URLs nestées.

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profil utilisateur
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),

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
]
