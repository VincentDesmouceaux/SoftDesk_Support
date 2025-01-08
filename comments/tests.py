"""
Tests pour l'application Comments, vérifiant la création, la mise à jour
et la suppression de commentaires liés à une issue.
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from authentication.models import CustomUser
from projects.models import Project
from issues.models import Issue
from comments.models import Comment


class CommentTests(APITestCase):
    """
    Classe de tests pour le ViewSet CommentViewSet.
    """

    def setUp(self):
        """
        Préparation de l'environnement de test :
        - Création d'utilisateurs
        - Création d'un projet + contributeurs
        - Création d'une issue
        - Authentification de l'utilisateur 'author'
        """
        self.author = CustomUser.objects.create_user(username='author', password='password123', age=30)
        self.contributor_user = CustomUser.objects.create_user(username='contributor', password='password123', age=25)
        self.other_user = CustomUser.objects.create_user(username='otheruser', password='password123', age=20)

        self.client.force_authenticate(user=self.author)

        self.project = Project.objects.create(
            title='Test Project',
            description='A simple test project',
            project_type='Back-End',
            author=self.author
        )
        self.project.contributors.add(self.author, self.contributor_user)

        self.issue = Issue.objects.create(
            title='Test Issue',
            description='A test issue description',
            tag='BUG',
            priority='HIGH',
            status='To Do',
            project=self.project,
            author=self.author
        )

        self.comment_list_url = reverse('issue-comments', kwargs={'project_id': self.project.id, 'issue_id': self.issue.id})

    def test_create_comment(self):
        """
        Vérifie la création d'un nouveau commentaire.
        """
        data = {
            'description': 'This is a comment'
        }
        response = self.client.post(self.comment_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_list_comments(self):
        """
        Vérifie la récupération de la liste des commentaires d'une issue.
        """
        Comment.objects.create(description='Comment 1', author=self.author, issue=self.issue)
        Comment.objects.create(description='Comment 2', author=self.contributor_user, issue=self.issue)

        response = self.client.get(self.comment_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_update_comment_by_author(self):
        """
        Vérifie qu'un auteur de commentaire peut mettre à jour son commentaire.
        """
        comment = Comment.objects.create(description='Original comment', author=self.author, issue=self.issue)
        comment_detail_url = reverse('issue-comment-detail', kwargs={
            'project_id': self.project.id,
            'issue_id': self.issue.id,
            'pk': comment.id
        })

        data = {'description': 'Updated comment'}
        response = self.client.patch(comment_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.description, 'Updated comment')

    def test_update_comment_by_non_author(self):
        """
        Vérifie qu'un non-auteur ne peut pas mettre à jour un commentaire.
        """
        comment = Comment.objects.create(description='Another comment', author=self.author, issue=self.issue)
        comment_detail_url = reverse('issue-comment-detail', kwargs={
            'project_id': self.project.id,
            'issue_id': self.issue.id,
            'pk': comment.id
        })

        self.client.force_authenticate(user=self.contributor_user)
        data = {'description': 'Attempted update'}
        response = self.client.patch(comment_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_by_author(self):
        """
        Vérifie qu'un auteur de commentaire peut le supprimer.
        """
        comment = Comment.objects.create(description='Comment to delete', author=self.author, issue=self.issue)
        comment_detail_url = reverse('issue-comment-detail', kwargs={
            'project_id': self.project.id,
            'issue_id': self.issue.id,
            'pk': comment.id
        })

        response = self.client.delete(comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_delete_comment_by_non_author(self):
        """
        Vérifie qu'un non-auteur ne peut pas supprimer un commentaire.
        """
        comment = Comment.objects.create(description='Comment not author', author=self.author, issue=self.issue)
        comment_detail_url = reverse('issue-comment-detail', kwargs={
            'project_id': self.project.id,
            'issue_id': self.issue.id,
            'pk': comment.id
        })

        self.client.force_authenticate(user=self.contributor_user)
        response = self.client.delete(comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_by_non_contributor(self):
        """
        Vérifie qu'un utilisateur non-contributeur ne peut pas accéder aux commentaires.
        """
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.comment_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
