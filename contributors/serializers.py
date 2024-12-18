from rest_framework import serializers
from .models import Contributor
from projects.models import Project
from authentication.models import CustomUser


class ContributorSerializer(serializers.ModelSerializer):
    # CHANGEMENT: Ajout de la précision du type de champ
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Contributor
        fields = ['user', 'project', 'role']
