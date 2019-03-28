#!/usr/bin/env python3

import os
import json

import pytest
import requests

from app import app


class TestConnexion:
    """The base test providing auth and flask clients to other tests
    """
    cache: dict = {}
    CENTRAL_NODE_BASE_URL = os.environ.setdefault('CENTRAL_NODE_BASE_URL', 'http://localhost:8080/api/v1')

    #@requests_mock.mock()
    @pytest.fixture(scope='function')
    def client(self, requests_mock):
        calendar_response = [{
            'payload': {
                "events": [
                {
                    "begin": "2019-03-28T18:17:00+00:00",
                    "categories": [],
                    "description": '',
                    "end": "2019-03-28T20:17:00+00:00",
                    "location": '',
                    "name": "Demo Event"
                }
            ]
            }
        }]

        with open('test/wikipedia.json', 'r') as wikipedia:
            wiki = json.load(wikipedia)

        wikipedia_response = [{
            'payload': wiki
        }]

        requests_mock.post(f'{self.CENTRAL_NODE_BASE_URL}/skill', text='', status_code=204)
        requests_mock.post(f'{self.CENTRAL_NODE_BASE_URL}/monitoring/calendar', json=calendar_response, status_code=200)
        requests_mock.post(f'{self.CENTRAL_NODE_BASE_URL}/monitoring/wikipedia', json=wikipedia_response, status_code=200)
        requests_mock.post(f'{self.CENTRAL_NODE_BASE_URL}/proactive', text='', status_code=204)
        with app.app.test_client() as c:
            yield c
