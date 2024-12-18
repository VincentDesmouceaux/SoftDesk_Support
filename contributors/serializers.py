# contributors/serializers.py
from rest_framework import serializers
from .models import Contributor
from projects.models import Project
from authentication.models import CustomUser
from rest_framework.reverse import reverse


class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    url = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ['url', 'user', 'project', 'role']

    def get_url(self, obj):
        request = self.context.get('request')
        # Construction manuelle de l'URL détail
        return reverse('project-contributor-detail',
                       kwargs={'project_id': str(obj.project.id), 'pk': obj.pk},
                       request=request)
