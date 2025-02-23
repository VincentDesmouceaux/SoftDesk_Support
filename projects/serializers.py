"""
Ce module définit les sérialiseurs (DRF) pour le modèle Project,
permettant de transformer les données de la base en JSON et inversement.
"""

from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    """
    Sérialiseur pour le modèle Project utilisant un HyperlinkedModelSerializer.
    Il inclut :
    - URL du projet
    - URL pour la liste des contributeurs
    - Auteur du projet (en lecture seule)
    """
    contributors_url = serializers.HyperlinkedIdentityField(
        view_name='project-contributors',
        lookup_field='id',
        lookup_url_kwarg='project_id'
    )

    author = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
        lookup_field='pk'
    )

    url = serializers.HyperlinkedIdentityField(
        view_name='project-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Project
        fields = [
            'id',
            'url',
            'title',
            'description',
            'project_type',
            'author',
            'created_time',
            'contributors_url'
        ]
        read_only_fields = ['id', 'author', 'created_time']
