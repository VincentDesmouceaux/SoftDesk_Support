"""
Configuration de l'application Comments.
"""

from django.apps import AppConfig


class CommentsConfig(AppConfig):
    """
    Classe de configuration pour l'application Comments.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "comments"
