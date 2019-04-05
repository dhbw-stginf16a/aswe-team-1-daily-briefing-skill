import json
import pytest

from .TestConnexion import TestConnexion


@pytest.mark.usefixtures('client')
class TestProactive(TestConnexion):
    """A demo test without real purpose
    """
    def test_proactiveNoPrefs(self, client, requests_mock):
        # No preferences
        requests_mock.get(f'{self.CENTRAL_NODE_BASE_URL}/preferences/user/DemoUser', status_code=200, json={})

        response = client.post('/api/v1/trigger/DemoUser')

        assert response.status_code == 204

    def test_proactivePrefs(self, client, requests_mock):
        userPrefs = {
            'pollen': 'ambrosia;graeser',
            'trello_board': 'abc',
            'calendarURL': 'http://some.url/calendar.ics',
            'wikipedia': 'deaths'
        }

        # All preferences
        requests_mock.get(f'{self.CENTRAL_NODE_BASE_URL}/preferences/user/DemoUser', status_code=200, json=userPrefs)
        response = client.post('/api/v1/trigger/DemoUser')

        assert response.status_code == 204
