#!/usr/bin/env python3

import logging

logger = logging.getLogger(__name__)

from api.models.BriefingManager import BRIEFING_MANAGER

def trigger():
    """This function is triggered by the api.
    """
    BRIEFING_MANAGER.run()

    return '', 204
