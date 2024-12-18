"""
WSGI config for SoftDesk_Support project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SoftDesk_Support.settings')

application = get_wsgi_application()
