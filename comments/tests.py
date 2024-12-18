from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from authentication.models import CustomUser
from projects.models import Project
from contributors.models import Contributor
from issues.models import Issue
from comments.models import Comment


class CommentTests(APITestCase):
    def setUp(self):
        # Création d'utilisateurs
        self.author = CustomUser.objects.create_user(username='author', password='password123', age=30)
        self.contributor_user = CustomUser.objects.create_user(username='contributor', password='password123', age=25)
        self.other_user = CustomUser.objects.create_user(username='otheruser', password='password123', age=20)

        # Authentification en tant qu'auteur
        self.client.force_authenticate(user=self.author)

        # Création d'un projet
        self.project = Project.objects.create(
            title='Test Project',
            description='A simple test project',
            project_type='Back-End',
            author=self.author
        )
        # L'auteur et le contributor_user sont contributeurs
        self.project.contributors.add(self.author, self.contributor_user)

        # Création d'une issue
        self.issue = Issue.objects.create(
            title='Test Issue',
            description='A test issue description',
            tag='BUG',
            priority='HIGH',
            status='To Do',
            project=self.project,
            author=self.author
        )

        # URLs pour les commentaires
        self.comment_list_url = reverse('issue-comments', kwargs={'project_id': self.project.id, 'issue_id': self.issue.id})

    def test_create_comment(self):
        """
        Test de la création d'un nouveau commentaire sur une issue.
        """
        data = {
            'description': 'This is a comment'
        }
        response = self.client.post(self.comment_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.description, 'This is a comment')
        self.assertEqual(comment.author, self.author)
        self.assertEqual(comment.issue, self.issue)

    def test_list_comments(self):
        """
        Test de la récupération de la liste des commentaires.
        """
        # Création de quelques commentaires
        Comment.objects.create(description='Comment 1', author=self.author, issue=self.issue)
        Comment.objects.create(description='Comment 2', author=self.contributor_user, issue=self.issue)

        response = self.client.get(self.comment_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_update_comment_by_author(self):
        """
        Test de la mise à jour d'un commentaire par son auteur.
        """
        comment = Comment.objects.create(description='Original comment', author=self.author, issue=self.issue)
        comment_detail_url = reverse('issue-comment-detail', kwargs={'project_id': self.project.id, 'issue_id': self.issue.id, 'pk': comment.id})

        data = {'description': 'Updated comment'}
        response = self.client.patch(comment_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.description, 'Updated comment')

    def test_update_comment_by_non_author(self):
        """
        Test qu'un non auteur (même contributeur) ne peut pas mettre à jour un commentaire.
        """
        comment = Comment.objects.create(description='Another comment', author=self.author, issue=self.issue)
        comment_detail_url = reverse('issue-comment-detail', kwargs={'project_id': self.project.id, 'issue_id': self.issue.id, 'pk': comment.id})

        # Authentification en tant qu'un autre contributeur
        self.client.force_authenticate(user=self.contributor_user)
        data = {'description': 'Attempted update'}
        response = self.client.patch(comment_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        comment.refresh_from_db()
        self.assertNotEqual(comment.description, 'Attempted update')

    def test_delete_comment_by_author(self):
        """
        Test de la suppression d'un commentaire par son auteur.
        """
        comment = Comment.objects.create(description='Comment to delete', author=self.author, issue=self.issue)
        comment_detail_url = reverse('issue-comment-detail', kwargs={'project_id': self.project.id, 'issue_id': self.issue.id, 'pk': comment.id})

        response = self.client.delete(comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_delete_comment_by_non_author(self):
        """
        Test qu'un non auteur (même si contributeur) ne peut pas supprimer un commentaire.
        """
        comment = Comment.objects.create(description='Comment not author', author=self.author, issue=self.issue)
        comment_detail_url = reverse('issue-comment-detail', kwargs={'project_id': self.project.id, 'issue_id': self.issue.id, 'pk': comment.id})

        # Authentification en tant qu'un autre contributeur
        self.client.force_authenticate(user=self.contributor_user)
        response = self.client.delete(comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), 1)

    def test_access_by_non_contributor(self):
        """
        Test qu'un utilisateur non contributeur du projet ne peut pas accéder aux commentaires.
        """
        # Authentification en tant qu'autre_user qui n'est pas contributeur
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.comment_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
