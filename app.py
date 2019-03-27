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


CENTRAL_NODE_BASE_URL = os.environ.setdefault('CENTRAL_NODE_BASE_URL', 'http://localhost:8080/api/v1')
OUR_URL = os.environ.setdefault('OWN_URL', 'http://localhost:5000')

app = connexion.App(__name__, specification_dir='openapi/')
app.add_api('openapi.yml')

# Set CORS headers
CORS(app.app)

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

logger.info('App initialized')
