from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from store_app.models import Product, Category
from rest_framework_simplejwt.tokens import RefreshToken

class ProductAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin123')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            description='Powerful laptop',
            price=1000,
            category=self.category
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_product_list(self):
        url = reverse('product-list')  # URL name in urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_product_detail(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Laptop')

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            'name': 'Smartphone',
            'description': 'Latest model',
            'price': 500,
            'category': self.category.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_update_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        data = {
            'name': 'Updated Laptop',
            'description': 'Updated desc',
            'price': 1200,
            'category': self.category.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Laptop')

    def test_delete_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
