from rest_framework import serializers
from .models import Project  # On n'importe plus Contributor ici


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'project_type', 'author', 'created_time']
        read_only_fields = ['id', 'author', 'created_time']
