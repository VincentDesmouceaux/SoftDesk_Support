"""
Fichier ASGI pour le projet SoftDesk_Support.
Ce fichier expose une application ASGI permettant aux serveurs compatibles ASGI de servir le projet.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SoftDesk_Support.settings')

application = get_asgi_application()
