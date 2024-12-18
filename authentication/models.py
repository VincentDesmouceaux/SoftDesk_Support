from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None or 'password' in self.get_dirty_fields():
            if self.password and not self.password.startswith("pbkdf2_sha256$"):
                self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
