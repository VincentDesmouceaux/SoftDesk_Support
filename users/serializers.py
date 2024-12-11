from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'age', 'can_be_contacted', 'can_data_be_shared', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # Le mot de passe est uniquement en écriture
        }

    def create(self, validated_data):
        # Crée un utilisateur avec le mot de passe haché
        user = CustomUser.objects.create(**validated_data)
        return user
