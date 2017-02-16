from django.test import Client

import requests

import httpretty

import os

import unittest

from django_webtest import WebTest

SOCIAL_AUTH_DRCHRONO_KEY = os.environ['SOCIAL_AUTH_DRCHRONO_KEY']

#testing requirements/suggestions taken from https://python-social-auth-docs.readthedocs.io/en/latest/tests.html

class ServerBackendTestCases(unittest.TestCase):
	"""Testing access to API via mock HTTP client library"""

	@httpretty.activate
	def test_HTTP(self):

		httpretty.register_uri(httpretty.GET, 'https://drchrono.com/o/authorize/', {
			'redirect_uri': 'http://localhost:8000/', 'response_type': 'code', 'client_id': SOCIAL_AUTH_DRCHRONO_KEY})
		response = requests.get('https://drchrono.com/o/authorize/?redirect_uri=http://localhost:8000/')
		self.assertEqual(response.status_code, 200)

class NotLoggedInTestCases(unittest.TestCase):
	"""Test main page and reminder page when application not yet authorized"""

	def setUp(self):
		self.client = Client()

	def test_NotLoggedinBirthdays(self):
		result = self.client.get('/reminder')
		self.assertIn('To use this feature, please authorize the application', result.content)
		self.assertNotIn('Do any of my patients have birthdays today?', result.content)

	def test_Home(self):
		result = self.client.get('/')
		self.assertIn('drchrono OAuth', result.content)

class LoggedInTestCases(WebTest):
	"""Test reminder page when application has been authorized"""

	def test_Loggedin(self):
		pass


		







