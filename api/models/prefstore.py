#!/usr/bin/env python3

import logging
import os

import requests

logger = logging.getLogger(__name__)


CENTRAL_NODE_BASE_URL = os.environ["CENTRAL_NODE_BASE_URL"]

class PrefStoreClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_user_prefs(self, user):
        r = requests.get("{}/preferences/user/{}".format(self.base_url, user), timeout=10)
        assert r.status_code == 200
        return r.json()

PREFSTORE_CLIENT = PrefStoreClient(CENTRAL_NODE_BASE_URL)


def getCalendarURL(calendarName):
    userPrefs = PREFSTORE_CLIENT.get_user_prefs(calendarName)
    return userPrefs['calendarURL']
