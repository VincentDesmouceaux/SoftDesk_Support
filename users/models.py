from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Hachage du mot de passe si nécessaire
        if self.pk is None or 'password' in self.get_dirty_fields():  # Vérifie si l'utilisateur est nouveau ou si le mot de passe est modifié
            if self.password and not self.password.startswith('pbkdf2_sha256$'):  # Hachage uniquement si le mot de passe n'est pas déjà haché
                self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
