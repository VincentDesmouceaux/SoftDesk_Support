"""
Modèle Contributor représentant la participation d'un utilisateur à un projet
avec un rôle spécifique (lecture, écriture, etc.).
"""

from django.db import models
from django.conf import settings
from projects.models import Project


class Contributor(models.Model):
    """
    Modèle établissant la relation ManyToMany avec un champ 'role' entre un utilisateur et un projet.
    """
    READ = 'Read'
    WRITE = 'Write'

    ROLE_CHOICES = [
        (READ, 'Read'),
        (WRITE, 'Write'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contributions'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='project_contributor_links'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=READ
    )

    class Meta:
        unique_together = ('user', 'project')
        ordering = ['project', 'user']

    def __str__(self):
        """
        Représentation textuelle indiquant l'utilisateur, son rôle et le projet.
        """
        return f"{self.user.username} ({self.role}) in {self.project.title}"
