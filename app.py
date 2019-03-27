#!/usr/bin/env python3

import logging
import os
import time

import requests
import connexion
from flask_cors import CORS
from requests.exceptions import ConnectionError

from api.models.BriefingManager import BRIEFING_MANAGER

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


CENTRAL_NODE_BASE_URL = os.environ["CENTRAL_NODE_BASE_URL"]
OUR_URL = os.environ["OWN_URL"]

app = connexion.App(__name__, specification_dir='openapi/')
app.add_api('openapi.yml')

# Set CORS headers
CORS(app.app)

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

logger.info('App initialized')


# Try to register the application on app startup
@application.before_first_request
def register():
    while True:
        logger.info("Attempting registration")
        try:
            r = requests.post("{}/skill".format(CENTRAL_NODE_BASE_URL), json={ "name": "daily_briefing", "endpoint": OUR_URL, "interests": []})
            if r.status_code == 204:
                logger.info("Registered")
                break
        except ConnectionError as conn:
            logger.warning('Attempted registration failed: %s', conn)
            logger.warning('Retrying in 5 seconds')

        time.sleep(5)
    BRIEFING_MANAGER.run()
