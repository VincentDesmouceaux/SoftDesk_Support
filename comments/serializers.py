"""
Sérialiseur pour le modèle Comment, permettant de convertir les données en JSON et vice-versa.
"""

from rest_framework import serializers
from .models import Comment
from rest_framework.reverse import reverse


class CommentSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Comment.
    Les champs author et issue sont en lecture seule.
    """
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    issue = serializers.PrimaryKeyRelatedField(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'url', 'description', 'author', 'issue', 'created_time']
        read_only_fields = ['id', 'author', 'issue', 'created_time']

    def get_url(self, obj):
        """
        Construit l'URL de détail du commentaire, incluant l'ID du projet et l'ID de l'issue.
        """
        request = self.context.get('request')
        return reverse(
            'issue-comment-detail',
            kwargs={
                'project_id': str(obj.issue.project.id),
                'issue_id': str(obj.issue.id),
                'pk': str(obj.pk)
            },
            request=request
        )
