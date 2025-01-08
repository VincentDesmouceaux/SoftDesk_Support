"""
Modèle Comment représentant un commentaire sur une Issue.
"""

import uuid
from django.db import models
from django.conf import settings
from issues.models import Issue


class Comment(models.Model):
    """
    Modèle pour un commentaire lié à une issue.
    Chaque Comment a :
    - Un UUID comme identifiant
    - Une description
    - Un auteur (ForeignKey vers l'utilisateur)
    - Une issue (ForeignKey vers l'issue concernée)
    - Une date de création
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_comments'
    )
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Représentation textuelle : "Comment by <username> on <issue-title>"
        """
        return f"Comment by {self.author.username} on {self.issue.title}"
