import json
import pytest

from .TestConnexion import TestConnexion


@pytest.mark.usefixtures('client')
class TestProactive(TestConnexion):
    """A demo test without real purpose
    """
    def test_proactive(self, client):
        response = client.post('/api/v1/trigger/DemoUser')

        assert response.status_code == 204
