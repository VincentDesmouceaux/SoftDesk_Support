"""
Configuration de l'application Projects.
Permet de définir le nom de l'application et divers réglages spécifiques.
"""

from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    """
    Classe de configuration pour l'application Projects.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "projects"
