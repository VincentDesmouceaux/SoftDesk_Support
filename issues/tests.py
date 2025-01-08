from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from authentication.models import CustomUser
from projects.models import Project
from issues.models import Issue


class IssueTests(APITestCase):
    def setUp(self):
        self.author = CustomUser.objects.create_user(username='author', password='password123', age=30)
        self.other_user = CustomUser.objects.create_user(username='contributor', password='password123', age=20)
        self.client.force_authenticate(user=self.author)
        self.project = Project.objects.create(title='Test Project', description='test', project_type='Back-End', author=self.author)
        self.project.contributors.add(self.author, self.other_user)

        self.issue_list_url = reverse('project-issues', kwargs={'project_id': self.project.id})

    def test_create_issue(self):
        data = {
            'title': 'Issue 1',
            'description': 'A test issue',
            'tag': 'BUG',
            'priority': 'HIGH',
            'status': 'To Do'
        }
        response = self.client.post(self.issue_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Issue.objects.count(), 1)
