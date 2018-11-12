# -* encoding: utf-8 *-
import logging

from threading import Thread
from typing import Dict, List
from urllib.parse import urlparse, ParseResult

import consul

from django.conf import settings

from certbot_daemon.utils import certificate_exists, request_certificate


class ConsulMonitor(Thread):
    def __init__(self):
        super().__init__(name="Consul-Monitor", daemon=True)
        url = settings.CONSUL_URL if hasattr(settings, 'CONSUL_URL') else "http://127.0.0.1:8500/"
        pr = urlparse(url)  # type: ParseResult
        self.consul = consul.Consul(
            host=pr.hostname,
            port=pr.port,
            scheme=pr.scheme,
            token=settings.CONSUL_TOKEN,
            dc=settings.CONSUL_DC,
            verify=settings.CONSUL_VERIFY,
            cert=settings.CONSUL_CERT,
        )
        self._log = logging.getLogger(__name__)

    def run(self):
        index, _ = self.consul.catalog.services()

        while True:
            index, catalog = self.consul.catalog.services(
                index=index,
                wait='30m'
            )  # type: int, Dict[str, List[str]]

            self._log.debug("Woke up with index=%s", str(index))
            hostnames = []
            for service, tags in catalog.items():
                for tag in tags:
                    if tag.startswith("smartstack:hostname:"):
                        hostnames.append(tag[len("smartstack:hostname:"):])

            for hostname in hostnames:
                if not certificate_exists(hostname):
                    request_certificate(hostname)
