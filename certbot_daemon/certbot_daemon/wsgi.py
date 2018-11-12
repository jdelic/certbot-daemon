"""
WSGI config for certbot_daemon project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import logging

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.wsgi import get_wsgi_application

from certbot_daemon import cron
from certbot_daemon.consul_monitor import ConsulMonitor

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'certbot_daemon.settings')
application = get_wsgi_application()

_log = logging.getLogger(__name__)

_log.debug("Starting consul monitor thread...")
consul_monitor = ConsulMonitor()
consul_monitor.start()

_log.debug("Starting scheduler thread...")
cron_thread = BackgroundScheduler(timezone=pytz.UTC)
cron_thread.add_job(cron.check_for_renewals, 'interval', days=1)
cron_thread.start()
