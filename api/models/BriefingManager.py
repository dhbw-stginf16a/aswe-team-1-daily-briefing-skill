import logging
import os
import threading
import time
from datetime import datetime

import requests

from api.models.motivationalQuotes import getMotivationalQuote

logger = logging.getLogger(__name__)

CENTRAL_NODE_BASE_URL = os.environ["CENTRAL_NODE_BASE_URL"]


class PeriodicSkillWorker:
    """This is a manager to constantly check daily updates
    """

    def __init__(self):
        """Init
        """
        self.run()

    def getCalendarEvents(self):
        body = {
            'type': 'event_date',
            'payload': {
                'user': 'DemoUser',
                'date': datetime.now().isoformat()
            }
        }
        resp = requests.post(f'{CENTRAL_NODE_BASE_URL}/monitoring/calendar', json=body)
        return resp.json()['payload']

    def getTrelloCards(self):
        return [{'Task': 'ASWE Presentation', 'dueDate': datetime.today().isoformat()}]

    def getWikipediaData(self):
        body = {
            'type': 'event_on_this_day',
            'payload': {
                'type': 'all',
                'day': 'today'
            }
        }
        resp = requests.post(f'{CENTRAL_NODE_BASE_URL}/monitoring/wikipedia', json=body)
        return resp.json()['payload']

    def generateEvent(self):
        return {
            'type': 'daily_briefing',
            'payload': {
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
        requests.post(f'{CENTRAL_NODE_BASE_URL}/proactive', json=self.generateEvent())
        threading.Timer(24*3600, self.run).start()

BRIEFING_MANAGER = PeriodicSkillWorker()
