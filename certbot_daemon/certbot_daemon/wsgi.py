"""
WSGI config for certbot_daemon project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from certbot_daemon.consul_monitor import ConsulMonitor

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'certbot_daemon.settings')

application = get_wsgi_application()

consul_monitor = ConsulMonitor()
consul_monitor.start()
