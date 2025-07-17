# tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product, Category
from django.contrib.auth.models import User

class ProductViewSetTests(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Create test data
        self.category = Category.objects.create(
            name='Beverages',
            description='Drinks',
            is_active=True
        )
        self.product = Product.objects.create(
            name='Coffee',
            description='Hot coffee',
            price=2.50,
            category=self.category,
            is_available=True,
            preparation_time=5
        )
        self.unavailable_product = Product.objects.create(
            name='Out of Stock Item',
            description='Not available',
            price=10.00,
            category=self.category,
            is_available=False,
            preparation_time=10
        )
        # URLs
        self.list_url = reverse('product-list')
        self.detail_url = reverse('product-detail', args=[self.product.id])
        self.availability_url = reverse('product-check-availability', args=[self.product.id])
        self.unavailable_url = reverse('product-check-availability', args=[self.unavailable_product.id])
        
        # Authenticate
        self.client.force_authenticate(user=self.user)

    # CRUD Tests
    def test_list_products(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming pagination is enabled

    def test_retrieve_product(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)
        self.assertEqual(float(response.data['price']), float(self.product.price))

    def test_create_product(self):
        data = {
            'name': 'New Product',
            'description': 'New description',
            'price': '15.99',
            'category': self.category.id,
            'is_available': True,
            'preparation_time': 20
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(Product.objects.get(id=response.data['id']).name, 'New Product')

    def test_update_product(self):
        data = {'name': 'Updated Coffee', 'price': '3.50'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Coffee')
        self.assertEqual(float(self.product.price), 3.50)

    def test_delete_product(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)  # Only unavailable product left


    # Availability Check Tests
    def test_check_available_product(self):
        response = self.client.get(self.availability_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_id'], self.product.id)
        self.assertEqual(response.data['product_name'], self.product.name)
        self.assertTrue(response.data['is_available'])
        self.assertEqual(response.data['message'], 'Available for order')

    def test_check_unavailable_product(self):
        response = self.client.get(self.unavailable_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_id'], self.unavailable_product.id)
        self.assertEqual(response.data['product_name'], self.unavailable_product.name)
        self.assertFalse(response.data['is_available'])
        self.assertEqual(response.data['message'], 'Currently unavailable')

    def test_check_nonexistent_product(self):
        invalid_url = reverse('product-check-availability', args=[999])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
