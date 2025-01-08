"""
Sérialiseurs pour le modèle Issue, permettant la conversion vers/depuis JSON.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Issue
from rest_framework.reverse import reverse

User = get_user_model()


class IssueSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Issue.
    Les champs author, project sont en lecture seule.
    La clé assignee est facultative (peut être nulle).
    """
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            'id',
            'url',
            'title',
            'description',
            'tag',
            'priority',
            'status',
            'project',
            'author',
            'assignee',
            'created_time'
        ]
        read_only_fields = ['id', 'author', 'project', 'created_time']

    def get_url(self, obj):
        """
        Construit dynamiquement l'URL de détail pour l'issue en tenant compte du projet auquel elle appartient.
        """
        request = self.context.get('request')
        return reverse(
            'project-issue-detail',
            kwargs={'project_id': str(obj.project.id), 'pk': str(obj.pk)},
            request=request
        )
