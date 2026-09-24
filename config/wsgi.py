"""
Configuración WSGI para el proyecto 'config'.

Expone la variable a nivel de módulo `application`, que es lo que
Gunicorn usa para servir la aplicación (ver entrypoint.sh:
`gunicorn config.wsgi:application`).
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
