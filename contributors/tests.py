from rest_framework.test import APITestCase
from rest_framework import status
from authentication.models import CustomUser
from projects.models import Project
from contributors.models import Contributor


class ContributorTests(APITestCase):
    def setUp(self):
        # Création des utilisateurs
        self.author = CustomUser.objects.create_user(username='author', password='password123')
        self.contributor_user = CustomUser.objects.create_user(username='contributor', password='password123')

        # Création d'un projet
        self.project = Project.objects.create(
            title='Test Project',
            description='A simple test project',
            project_type='Back-End',
            author=self.author
        )

        # Ajout de l'auteur comme contributeur
        self.project.contributors.add(self.author)

        # Ajout d'un autre contributeur
        Contributor.objects.create(
            user=self.contributor_user,
            project=self.project,
            role='Read'
        )

        self.client.force_authenticate(user=self.author)

    def test_add_contributor(self):
        # Créer un nouvel utilisateur pour éviter la contrainte unique
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
        response = self.client.get(f'/api/projects/{self.project.id}/contributors/')
        print("\n[TEST DEBUG] test_list_contributors -> Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Le projet a désormais 2 contributeurs : l'auteur et le contributeur ajouté
        self.assertEqual(len(response.data['results']), 2)
