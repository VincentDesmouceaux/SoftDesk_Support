"""
Sérialiseur pour le modèle Contributor, permettant la transformation de l'objet Contributor
en JSON et inversement.
"""

from rest_framework import serializers
from .models import Contributor
from projects.models import Project
from authentication.models import CustomUser
from rest_framework.reverse import reverse


class ContributorSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Contributor.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    url = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ['url', 'user', 'project', 'role']

    def get_url(self, obj):
        """
        Construit l'URL de détail du contributeur en fonction de l'ID du projet et de l'ID du contributor.
        """
        request = self.context.get('request')
        return reverse(
            'project-contributor-detail',
            kwargs={'project_id': str(obj.project.id), 'pk': obj.pk},
            request=request
        )
