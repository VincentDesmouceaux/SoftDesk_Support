from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']  # Définit un tri par défaut par ID pour éviter les avertissements de pagination

    def save(self, *args, **kwargs):
        # Vérifie si l'utilisateur existe déjà
        if self.pk is not None:
            # Récupère l'utilisateur original pour comparer les champs
            original = CustomUser.objects.get(pk=self.pk)
            # Vérifie si le mot de passe a changé et s'il doit être haché
            if original.password != self.password and not self.password.startswith("pbkdf2_sha256$"):
                self.password = make_password(self.password)
        else:
            # Cas d'un nouvel utilisateur : rechercher le plus petit ID disponible
            existing_ids = set(CustomUser.objects.values_list('id', flat=True))
            if existing_ids:
                # Trouver le plus petit ID disponible
                new_id = min(set(range(1, max(existing_ids) + 2)) - existing_ids)
            else:
                new_id = 1  # Premier utilisateur
            self.id = new_id  # Assigner l'ID manuellement

            if self.password and not self.password.startswith("pbkdf2_sha256$"):
                self.password = make_password(self.password)

        # Appel à la méthode save de la classe parente
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
