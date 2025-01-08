#!/usr/bin/env python
"""
Fichier principal permettant d'exécuter les tâches administratives de Django via la ligne de commande.
Ce script sert notamment à lancer le serveur de développement, migrer la base de données,
créer des utilisateurs, etc.
"""

import os
import sys


def main():
    """
    Point d'entrée principal pour lancer les tâches administratives Django.
    Il définit la variable d'environnement DJANGO_SETTINGS_MODULE puis invoque
    la commande `execute_from_command_line` de Django.

    Raises:
        ImportError: Si Django n'est pas installé ou introuvable.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SoftDesk_Support.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossible d'importer Django. Assurez-vous qu'il est installé et accessible "
            "sur votre variable d'environnement PYTHONPATH. Avez-vous activé un environnement virtuel ?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
