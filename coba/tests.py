# coba/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class TestViewTests(APITestCase):
    def test_get_test_view(self):
        url = reverse('test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Hello World"})