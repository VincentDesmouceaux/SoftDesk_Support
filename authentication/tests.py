from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from authentication.models import CustomUser


class UserTests(APITestCase):
    def setUp(self):
        """
        Configuration initiale avant chaque test.
        """
        CustomUser.objects.all().delete()  # Supprime toutes les données pour éviter les conflits
        self.existing_user = CustomUser.objects.create_superuser(
            username="existinguser",
            email="existinguser@example.com",
            password="password123",
            age=30
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
            "password": "password123",
            "age": 20
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_list_users(self):
        """
        Test de la récupération de la liste des utilisateurs.
        """
        self.client.force_authenticate(user=self.existing_user)
        response = self.client.get(self.create_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_user(self):
        """
        Test de mise à jour partielle d'un utilisateur.
        """
        url = reverse('user-detail', kwargs={'pk': self.existing_user.pk})
        data = {"email": "updatedemail@example.com"}
        self.client.force_authenticate(user=self.existing_user)
        response = self.client.patch(url, data, format='json')
        print(f"PATCH response status: {response.status_code}, data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_user_not_allowed(self):
        other_user = CustomUser.objects.create_user(
            username="unique_otheruser",
            email="otheruser@example.com",
            password="password123",
            age=25
        )
        normal_user = CustomUser.objects.create_user(
            username="normaluser",
            email="normaluser@example.com",
            password="password123",
            age=40
        )

        url = reverse('user-detail', kwargs={'pk': other_user.pk})
        data = {"email": "hackedemail@example.com"}

        # Authentification en tant qu'utilisateur normal, pas superuser
        self.client.force_authenticate(user=normal_user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Vérifie que les données n'ont pas été modifiées
        other_user.refresh_from_db()
        self.assertNotEqual(other_user.email, "hackedemail@example.com")
