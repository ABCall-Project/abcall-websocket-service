import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from http import HTTPStatus
from flaskr.endpoint.healthCheck.HealthCheck import HealthCheck

class TestHealthCheck(unittest.TestCase):

    def setUp(self):

        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(HealthCheck, '/health')
        self.client = self.app.test_client()  

    def test_get_healthcheck(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, HTTPStatus.OK)


