from django.test import TestCase
import unittest
# Create your tests here.

from django.test import Client

class SimpleTest(unittest.TestCase):
    def test_details(self):
        client = Client()
        response = client.get('/make_recognition/')
        self.assertEqual(response.status_code, 200)