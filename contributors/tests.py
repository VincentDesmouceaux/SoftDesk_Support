"""
Tests pour l'application Contributors, testant la création, la liste et la suppression
d'un contributeur dans un projet.
"""

from rest_framework.test import APITestCase
from rest_framework import status
from authentication.models import CustomUser
from projects.models import Project
from contributors.models import Contributor


class ContributorTests(APITestCase):
    """
    Classe de tests pour les endpoints relatifs aux Contributors.
    """

    def setUp(self):
        """
        Préparation du contexte de test :
        - Création de plusieurs utilisateurs
        - Création d'un projet
        - Création d'un contributor
        - Authentification de l'auteur
        """
        self.author = CustomUser.objects.create_user(username='author', password='password123')
        self.contributor_user = CustomUser.objects.create_user(username='contributor', password='password123')

        self.project = Project.objects.create(
            title='Test Project',
            description='A simple test project',
            project_type='Back-End',
            author=self.author
        )
        self.project.contributors.add(self.author)

        Contributor.objects.create(
            user=self.contributor_user,
            project=self.project,
            role='Read'
        )

        self.client.force_authenticate(user=self.author)

    def test_add_contributor(self):
        """
        Vérifie qu'on peut ajouter un nouveau contributeur à un projet.
        """
        new_user = CustomUser.objects.create_user(username='newcontributor', password='password123')
        data = {
            'user': new_user.id,
            'project': str(self.project.id),
            'role': 'Write'
        }
        print("\n[TEST DEBUG] Sending POST to add contributor with data:", data)
        response = self.client.post(f'/api/projects/{self.project.id}/contributors/', data, format='json')
        print("[TEST DEBUG] Response status:", response.status_code)
        print("[TEST DEBUG] Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_contributors(self):
        """
        Vérifie que la liste des contributeurs du projet est correctement retournée.
        """
        response = self.client.get(f'/api/projects/{self.project.id}/contributors/')
        print("\n[TEST DEBUG] test_list_contributors -> Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
