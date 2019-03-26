#!/usr/bin/env python3

import os

import pytest
import requests

from app import app


class TestConnexion:
    """The base test providing auth and flask clients to other tests
    """
    cache: dict = {}

    #@requests_mock.mock()
    @pytest.fixture(scope='function')
    def client(self, requests_mock):
        CENTRAL_NODE_BASE_URL = os.environ["CENTRAL_NODE_BASE_URL"]
        requests_mock.post(f'{CENTRAL_NODE_BASE_URL}/skill', text='', status_code=204)
        with app.app.test_client() as c:
            yield c
