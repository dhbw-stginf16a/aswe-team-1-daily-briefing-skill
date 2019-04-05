import json
import logging
import os
import threading
import time
from datetime import datetime

import requests

from api.models.motivationalQuotes import getMotivationalQuote
from api.models.songsOfTheDay import getSong
from api.models.prefstore import PREFSTORE_CLIENT

logger = logging.getLogger(__name__)

CENTRAL_NODE_BASE_URL = os.environ.setdefault('CENTRAL_NODE_BASE_URL', 'http://localhost:8080/api/v1')


class PeriodicSkillWorker:
    """This is a manager to constantly check daily updates
    """
    def getCalendarEvents(self, userName):
        body = {
            'type': 'event_date',
            'payload': {
                'user': userName,
                'date': datetime.now().isoformat()
            }
        }
        resp = requests.post(f'{CENTRAL_NODE_BASE_URL}/monitoring/calendar', json=body).json()
        logger.debug(resp[0]['payload'])
        return resp[0].setdefault('payload', {})

    def getTrelloCards(self, userName):
        body = {
            'type': 'cards_due_until',
            'payload': {
                'user': userName,
                'date': datetime.now().isoformat()
            }
        }
        resp = requests.post(f'{CENTRAL_NODE_BASE_URL}/monitoring/trello', json=body).json()
        logger.debug(resp[0]['payload'])
        return resp[0].setdefault('payload', {})

    def getWikipediaData(self, userPrefs):
        body = {
            'type': 'event_on_this_day',
            'payload': {
                'type': userPrefs.setdefault('wikipedia', 'all'),
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

    def getPollinationInfo(self, allergies):
        pollen = { allergy: 'true' for allergy in allergies }

        body = {
            'type': 'current_pollination',
            'payload': {
                "region": "Hohenlohe/mittlerer Neckar/Oberschwaben",
                "day": "today",
                "pollen": pollen
            }
        }

        resp = requests.post(f'{CENTRAL_NODE_BASE_URL}/monitoring/pollination', json=body).json()
        logger.debug(resp[0]['payload'])
        return resp[0].setdefault('payload', {})


    def generateEvent(self, userName):
        userPrefs = PREFSTORE_CLIENT.get_user_prefs(userName)
        payload =  {
            'user': userName,
            'song_of_the_day': getSong(),
            'wikipedia_events': self.getWikipediaData(userPrefs),
            'motivational_quote': getMotivationalQuote(),
        }

        if userPrefs.setdefault('calendarURL', None) is not None:
            payload['calendar_events'] = self.getCalendarEvents(userName)
        else:
            payload.setdefault('missing_credentials', list()).append('calendar')

        if userPrefs.setdefault('trello_board', None) is not None:
            payload['todo'] = self.getTrelloCards(userName)['cards']
        else:
            payload.setdefault('missing_credentials', list()).append('trello')

        if userPrefs.setdefault('pollen', None) is not None:
            allergies = userPrefs['pollen'].split(';')
            payload['pollen'] = self.getPollinationInfo(allergies)['pollination']
        else:
            payload.setdefault('missing_credentials', list()).append('pollen')

        return {
            'type': 'daily_briefing',
            'payload': payload
        }

    def run(self, userName):
        """Process a request
        """
        event = self.generateEvent(userName)
        print(json.dumps(event, indent=4, sort_keys=True))
        requests.post(f'{CENTRAL_NODE_BASE_URL}/proactive', json=event)
        # threading.Timer(24*3600, self.run).start()

BRIEFING_MANAGER = PeriodicSkillWorker()
