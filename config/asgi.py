"""
Configuración ASGI para el proyecto 'config'.
No se usa en este proyecto (Gunicorn corre en modo WSGI), pero se
incluye por si en el futuro se necesita soporte async/websockets.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
