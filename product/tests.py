import json
from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from django.db import connection


class ProductViewSetTests(TestCase):

    def setUp(self):
        """Menyiapkan database sebelum setiap pengujian."""
        self.client = Client()

        # Buat tabel siswa jika belum ada
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tb_product (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kd_product TEXT NOT NULL,
                    nm_product TEXT NOT NULL,
                    price REAL NOT NULL
                )
            """)

        # Masukkan data dummy untuk pengujian (dilakukan dalam blok with yang berbeda)
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO tb_product (kd_product, nm_product, price)
                VALUES (%s, %s, %s)
            """, ['P001', 'Produk Satu', 10000])
            self.product_id = cursor.lastrowid
            print({self.product_id})

    def tearDown(self):
        """Membersihkan database setelah pengujian."""
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM tb_product")

    def test_list_product(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('data', response.data)

    def test_retrieve_product(self):
        url = reverse('product-detail', args=[self.product_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['kd_product'], 'P001')

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            'kd_product': 'P002',
            'nm_product': 'Produk Dua',
            'price': 20000
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Product Created')

    def test_update_product(self):
        url = reverse('product-detail', args=[self.product_id])
        data = {
            'kd_product': 'P001U',
            'nm_product': 'Produk Update',
            'price': 15000
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Product Updated')
        self.assertEqual(response.data['data']['kd_product'], 'P001U')

    def test_delete_product(self):
        url = reverse('product-detail', args=[self.product_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], 'Product Deleted')

