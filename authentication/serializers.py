from rest_framework import serializers
from authentication.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'age', 'can_be_contacted', 'can_data_be_shared', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # Le mot de passe ne sera pas retourné dans les réponses
        }

    def create(self, validated_data):
        # Hache automatiquement le mot de passe lors de la création
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
