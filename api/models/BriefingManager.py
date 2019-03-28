import json
import logging
import os
import threading
import time
from datetime import datetime

import requests

from api.models.motivationalQuotes import getMotivationalQuote

logger = logging.getLogger(__name__)

CENTRAL_NODE_BASE_URL = os.environ.setdefault('CENTRAL_NODE_BASE_URL', 'http://localhost:8080/api/v1')


class PeriodicSkillWorker:
    """This is a manager to constantly check daily updates
    """
    def getCalendarEvents(self):
        body = {
            'type': 'event_date',
            'payload': {
                'user': 'DemoUser',
                'date': datetime.now().isoformat()
            }
        }
        resp = requests.post(f'{CENTRAL_NODE_BASE_URL}/monitoring/calendar', json=body).json()
        logger.debug(resp[0]['payload'])
        return resp[0].setdefault('payload', {})

    def getTrelloCards(self):
        return [{'Task': 'ASWE Presentation', 'dueDate': datetime.now().isoformat()}]

    def getWikipediaData(self):
        body = {
            'type': 'event_on_this_day',
            'payload': {
                'type': 'all',
                'day': 'today'
            }
        }
        resp = requests.post(f'{CENTRAL_NODE_BASE_URL}/monitoring/wikipedia', json=body).json()
        logger.debug(resp[0]['payload'])

        small_wiki = {}
        for key, value in resp[0]['payload'].items():
            small_wiki[key] = list()
            for element in value:
                small_wiki[key].append(element[0])
        return small_wiki

    def generateEvent(self):
        return {
            'type': 'daily_briefing',
            'payload': {
                'user': 'DemoUser',
                'song_of_the_day': 'https://www.youtube.com/watch?v=hPUvhMSRmUg',
                'calendar_events': self.getCalendarEvents(),
                'wikipedia_events': self.getWikipediaData(),
                'todo': self.getTrelloCards(),
                'motivational_quote': getMotivationalQuote()
            }
        }

    def run(self):
        """Process a request
        """
        event = self.generateEvent()
        logger.debug(json.dumps(event, indent=4, sort_keys=True))
        requests.post(f'{CENTRAL_NODE_BASE_URL}/proactive', json=event)
        # threading.Timer(24*3600, self.run).start()

BRIEFING_MANAGER = PeriodicSkillWorker()
