"""
ASGI config for SoftDesk_Support project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SoftDesk_Support.settings')

application = get_asgi_application()
