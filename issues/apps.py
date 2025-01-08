"""
Configuration de l'application Issues, gérant les tickets.
"""

from django.apps import AppConfig


class IssuesConfig(AppConfig):
    """
    Classe de configuration pour l'application Issues.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "issues"
