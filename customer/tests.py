#/customer/tests.py
import json
from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from django.db import connection

class CustomerViewSetTests(TestCase):
    def setUp(self):
        self.client = Client()
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tb_customer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nm_customer TEXT NOT NULL,
                    alamat TEXT NOT NULL,
                    email TEXT NOT NULL,
                    nohp TEXT NOT NULL
                )
            """)
            cursor.execute("""
                INSERT INTO tb_customer (nm_customer, alamat, email, nohp)
                VALUES (%s, %s, %s, %s)
            """, ['edy1', 'Semarang1', 'edy1@gmail.com', '08122888881'])
            self.customer_id = cursor.lastrowid

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM tb_customer")

    def test_list_customers(self):
        url = reverse('customer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_customer(self):
        url = reverse('customer-detail', args=[self.customer_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['nm_customer'], 'edy1')

    def test_create_customer(self):
        url = reverse('customer-list')
        data = {
            'nm_customer': 'edy2',
            'alamat': 'Semarang2',
            'email': 'edy2@gmail.com',
            'nohp': '08122888882',
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_customer(self):
        url = reverse('customer-detail', args=[self.customer_id])
        data = {
            'nm_customer': 'edy1 updated',
            'alamat': 'Jakarta',
            'email': 'edy1_new@gmail.com',
            'nohp': '08122999999',
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_customer(self):
        url = reverse('customer-detail', args=[self.customer_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)