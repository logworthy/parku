"""
WSGI config for parku project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os

PARKU_PATH = '/opt/parku/src/'

import sys
if not PARKU_PATH in sys.path:
    sys.path.append(PARKU_PATH)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parku.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
