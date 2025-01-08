"""
Fichier WSGI pour le projet SoftDesk_Support.
Ce fichier expose une application WSGI pour que les serveurs web compatibles WSGI
puissent servir le projet Django.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SoftDesk_Support.settings')

application = get_wsgi_application()
