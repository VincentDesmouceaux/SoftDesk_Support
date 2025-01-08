"""
Sérialiseur pour le modèle CustomUser, permettant notamment la création d'utilisateurs
et la validation de l'âge minimal.
"""

from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Sérialiseur pour le modèle CustomUser.
    Les champs sensibles (password) ne sont jamais renvoyés en clair.
    On utilise un HyperlinkedIdentityField pour le champ url.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='user-detail',
        lookup_field='pk'
    )

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'url',
            'username',
            'email',
            'age',
            'can_be_contacted',
            'can_data_be_shared',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_age(self, value):
        """
        Valide que l'utilisateur a au moins 15 ans.
        """
        if value < 15:
            raise serializers.ValidationError("L'utilisateur doit avoir au moins 15 ans.")
        return value

    def create(self, validated_data):
        """
        Crée un nouvel utilisateur avec un mot de passe haché.
        """
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
