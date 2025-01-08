"""
Ce module définit le modèle Project, qui représente un projet dans l'application.
Un projet possède un titre, une description, un type de projet (back-end, front-end, etc.),
un auteur et une date de création. Il peut avoir plusieurs contributeurs.
"""

import uuid
from django.db import models
from django.conf import settings


class Project(models.Model):
    """
    Modèle représentant un projet dans SoftDesk.
    Un projet est identifié par un UUID, possède un titre et une description, ainsi qu'un auteur.
    """
    BACKEND = 'Back-End'
    FRONTEND = 'Front-End'
    IOS = 'iOS'
    ANDROID = 'Android'

    PROJECT_TYPE_CHOICES = [
        (BACKEND, 'Back-End'),
        (FRONTEND, 'Front-End'),
        (IOS, 'iOS'),
        (ANDROID, 'Android'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPE_CHOICES)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_projects'
    )
    created_time = models.DateTimeField(auto_now_add=True)

    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='contributors.Contributor',
        related_name='project_contributors'
    )

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        """
        Renvoie la représentation en chaîne de caractères du projet, ici son titre.
        """
        return self.title
