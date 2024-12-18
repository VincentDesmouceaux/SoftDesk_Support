from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from authentication.models import CustomUser


class UserTests(APITestCase):
    def setUp(self):
        """
        Configuration initiale avant chaque test.
        """
        self.existing_user = CustomUser.objects.create_superuser(
            username="existinguser",
            email="existinguser@example.com",
            password="password123"
        )
        self.create_url = reverse('user-list')

    def tearDown(self):
        """
        Nettoyage après chaque test.
        """
        CustomUser.objects.all().delete()

    def test_create_user(self):
        """
        Test de création d'un nouvel utilisateur.
        """
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)  # 1 utilisateur existant + 1 nouvel utilisateur

    def test_list_users(self):
        """
        Test de la récupération de la liste des utilisateurs.
        """
        self.client.force_authenticate(user=self.existing_user)  # Authentification
        response = self.client.get(self.create_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # Vérifie qu'il y a au moins un utilisateur

    def test_duplicate_username(self):
        """
        Test pour vérifier que les noms d'utilisateur dupliqués ne sont pas autorisés.
        """
        data = {
            "username": "existinguser",  # Utilisateur déjà présent dans la base
            "email": "duplicate@example.com",
            "password": "password123"
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_patch_user(self):
        """
        Test de mise à jour partielle d'un utilisateur.
        """
        url = reverse('user-detail', kwargs={'pk': self.existing_user.pk})  # URL pour modifier l'utilisateur existant
        data = {"email": "updatedemail@example.com"}
        self.client.force_authenticate(user=self.existing_user)  # Authentification
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.existing_user.refresh_from_db()
        self.assertEqual(self.existing_user.email, "updatedemail@example.com")
