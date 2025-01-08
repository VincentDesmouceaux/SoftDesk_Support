"""
Modèle CustomUser étendant le AbstractUser de Django.
Permet d'ajouter des champs comme l'âge, et d'ajuster la logique d'ID et de mot de passe.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password


class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé avec champs supplémentaires :
    - age
    - can_be_contacted
    - can_data_be_shared
    - Système de génération d'ID minimaliste (pas forcément optimal en production).
    """
    age = models.PositiveIntegerField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour gérer :
        - Le hachage du mot de passe
        - L'attribution d'un ID incrémental (non standard)
        """
        if self.pk is not None:
            original = CustomUser.objects.get(pk=self.pk)
            if original.password != self.password and not self.password.startswith("pbkdf2_sha256$"):
                self.password = make_password(self.password)
        else:
            existing_ids = set(CustomUser.objects.values_list('id', flat=True))
            if existing_ids:
                new_id = min(set(range(1, max(existing_ids) + 2)) - existing_ids)
            else:
                new_id = 1
            self.id = new_id
            if self.password and not self.password.startswith("pbkdf2_sha256$"):
                self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Renvoie le nom d'utilisateur comme représentation en chaîne.
        """
        return self.username
