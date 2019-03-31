#!/usr/bin/env python3

import logging
import os

import requests

logger = logging.getLogger(__name__)


CENTRAL_NODE_BASE_URL = os.environ.setdefault('CENTRAL_NODE_BASE_URL', 'http://localhost:8080/api/v1')

class PrefStoreClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_user_prefs(self, user):
        r = requests.get("{}/preferences/user/{}".format(self.base_url, user), timeout=10)
        assert r.status_code == 200
        return r.json()

PREFSTORE_CLIENT = PrefStoreClient(CENTRAL_NODE_BASE_URL)
