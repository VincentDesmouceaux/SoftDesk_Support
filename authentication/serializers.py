from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'age', 'can_be_contacted', 'can_data_be_shared', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # Le mot de passe est uniquement en écriture
        }

    def validate_age(self, value):
        """
        Valide que l'utilisateur a au moins 15 ans.
        """
        if value < 15:
            raise serializers.ValidationError("L'utilisateur doit avoir au moins 15 ans pour s'inscrire.")
        return value

    def create(self, validated_data):
        """
        Crée un utilisateur avec le mot de passe haché.
        """
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
