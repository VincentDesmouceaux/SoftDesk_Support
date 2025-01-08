"""
Ce module contient les tests unitaires et d'intégration pour l'application Projects,
testant le bon fonctionnement des endpoints liés aux projets.
"""

from rest_framework.test import APITestCase
from rest_framework import status
from authentication.models import CustomUser
from projects.models import Project


class ProjectTests(APITestCase):
    """
    Classe de tests pour le ViewSet ProjectViewSet.
    On teste la création, la liste, etc.
    """

    def setUp(self):
        """
        Prépare l'environnement de test :
        - Création d'un utilisateur
        - Création d'un projet
        - Authentification forcée
        """
        self.user = CustomUser.objects.create_user(username='user', password='password123')
        self.project = Project.objects.create(
            title='Test Project',
            description='A simple test project',
            project_type='Back-End',
            author=self.user
        )
        self.project.contributors.add(self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_project(self):
        """
        Vérifie que la création d'un projet via POST sur /api/projects/ fonctionne.
        """
        data = {
            'title': 'New Project',
            'description': 'A new test project',
            'project_type': 'Front-End',
        }
        print("\n[TEST DEBUG] test_create_project -> POST data:", data)
        response = self.client.post('/api/projects/', data, format='json')
        print("[TEST DEBUG] test_create_project -> Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_projects(self):
        """
        Vérifie que la liste des projets est correctement retournée en GET /api/projects/.
        """
        print("\n[TEST DEBUG] test_list_projects -> GET /api/projects/")
        response = self.client.get('/api/projects/')
        print("[TEST DEBUG] test_list_projects -> Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
