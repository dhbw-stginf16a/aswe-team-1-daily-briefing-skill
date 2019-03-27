#!/usr/bin/env python3

import logging

logger = logging.getLogger(__name__)

from api.models.BriefingManager import BRIEFING_MANAGER

def trigger(body):
    """This function is triggered by the api.
    """
    logger.info(body)
    BRIEFING_MANAGER.run()

    return '', 204
