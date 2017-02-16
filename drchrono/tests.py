from django.test.client import Client

from django.conf import settings

from django.utils.importlib import import_module

import requests

import httpretty

import os

import unittest

from django.test import LiveServerTestCase

from selenium import webdriver

import time

SOCIAL_AUTH_DRCHRONO_KEY = os.environ['SOCIAL_AUTH_DRCHRONO_KEY']
PASSWORD = os.environ['DR_CHRONO_SITE_PASS']

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

class LoggedInTestCases(LiveServerTestCase):
	"""Test reminder page when application has been authorized"""

	def test_Loggedin(self):

		driver = webdriver.Chrome('/Users/taliatrilling/Downloads/chromedriver') 
		time.sleep(5);
		driver.get('http://localhost:8000/')
		time.sleep(5);
		btn = driver.find_element_by_id('auth')
		btn.click()
		username = driver.find_element_by_id('username')
		username.send_keys('taliatrilling')
		password = driver.find_element_by_id('password')
		password.send_keys(PASSWORD)
		login = driver.find_element_by_id('login')
		login.submit()
		cookies = driver.get_cookies()
		for cookie in cookies:
			print cookie
	
		# #driver.quit()








