from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import json
from polls.models import ItemType, IndividualItems, ShoppingList
from polls.middleware import APIAuthMiddleware
from polls.auth import NoPasswordBackend

class ModelTests(TestCase):
    def setUp(self):
        self.item_type = ItemType.objects.create(
            name="Test Item",
            unique_barcode="12345",
            amount_type="pieces"
        )

    def test_item_type_str(self):
        """Test ItemType string representation"""
        self.assertEqual(str(self.item_type), "Test Item")

    def test_individual_items(self):
        """Test IndividualItems model"""
        item = IndividualItems.objects.create(
            item_type=self.item_type,
            amount=5,
            expiration_date=timezone.now().date()
        )
        self.assertEqual(str(item), "Test Item (5)")

    def test_shopping_list(self):
        """Test ShoppingList model"""
        shopping_item = ShoppingList.objects.create(
            item_type=self.item_type,
            amount=3
        )
        self.assertEqual(shopping_item.amount, 3)

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.item_type = ItemType.objects.create(
            name="Test Item",
            unique_barcode="12345",
            amount_type="pieces"
        )
        self.user = User.objects.create_user(username='testuser')
        self.client.force_login(self.user)

    def test_index_view(self):
        """Test index view"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/index.html')

    def test_inventory_list_view(self):
        """Test inventory list view"""
        response = self.client.get(reverse('polls:inventory_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/inventory_list.html')

    def test_grid_view(self):
        """Test grid view"""
        response = self.client.get(reverse('polls:grid_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/grid_view.html')

    def test_shopping_list_view(self):
        """Test shopping list view"""
        response = self.client.get(reverse('polls:shopping_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/shopping_list.html')

    def test_add_to_inventory_view(self):
        """Test add to inventory view"""
        response = self.client.get(reverse('polls:add_to_inventory'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/add_to_inventory.html')

class APITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.item_type = ItemType.objects.create(
            name="Test Item",
            unique_barcode="12345",
            amount_type="pieces"
        )
        self.user = User.objects.create_user(username='testuser')
        self.client.force_login(self.user)

    def test_api_add_to_inventory(self):
        """Test API endpoint for adding to inventory"""
        data = {
            'itemType': '12345',
            'amount': 5,
            'expirationDate': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        }
        response = self.client.post(
            reverse('polls:api_add_to_inventory'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(IndividualItems.objects.filter(item_type=self.item_type).exists())

    def test_api_remove_from_inventory(self):
        """Test API endpoint for removing from inventory"""
        item = IndividualItems.objects.create(
            item_type=self.item_type,
            amount=5,
            expiration_date=timezone.now().date()
        )
        response = self.client.delete(
            reverse('polls:api_remove_from_inventory'),
            json.dumps({'itemId': item.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(IndividualItems.objects.filter(id=item.id).exists())

    def test_api_add_to_shopping_list(self):
        """Test API endpoint for adding to shopping list"""
        data = {
            'itemType': '12345',
            'amount': 3
        }
        response = self.client.put(
            reverse('polls:api_add_to_shopping_list'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ShoppingList.objects.filter(item_type=self.item_type).exists())

    def test_api_remove_from_shopping_list(self):
        """Test API endpoint for removing from shopping list"""
        ShoppingList.objects.create(
            item_type=self.item_type,
            amount=3
        )
        response = self.client.delete(
            reverse('polls:api_remove_from_shopping_list'),
            json.dumps({'itemType': '12345'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ShoppingList.objects.filter(item_type=self.item_type).exists())

    def test_api_purchase_item(self):
        """Test API endpoint for purchasing items"""
        ShoppingList.objects.create(
            item_type=self.item_type,
            amount=3
        )
        data = {
            'itemType': '12345',
            'amount': 2,
            'expirationDate': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        }
        response = self.client.patch(
            reverse('polls:api_purchase_item'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(IndividualItems.objects.filter(item_type=self.item_type).exists())
        self.assertFalse(ShoppingList.objects.filter(item_type=self.item_type).exists())

class MiddlewareTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_api_auth_middleware_csrf_missing(self):
        """Test APIAuthMiddleware CSRF protection"""
        response = self.client.post('/api/v1/test')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content), {'error': 'CSRF token missing'})

    def test_api_auth_middleware_non_api_request(self):
        """Test APIAuthMiddleware for non-API requests"""
        response = self.client.get('/')
        self.assertNotEqual(response.status_code, 403)

class AuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.backend = NoPasswordBackend()

    def test_authenticate_valid_user(self):
        """Test NoPasswordBackend with valid username"""
        authenticated_user = self.backend.authenticate(None, username='testuser')
        self.assertEqual(authenticated_user, self.user)

    def test_authenticate_invalid_user(self):
        """Test NoPasswordBackend with invalid username"""
        authenticated_user = self.backend.authenticate(None, username='nonexistent')
        self.assertIsNone(authenticated_user)

class AppConfigTests(TestCase):
    def test_apps_config(self):
        """Test PollsConfig"""
        from polls.apps import PollsConfig
        self.assertEqual(PollsConfig.name, 'polls')

class APIConfigTests(TestCase):
    def test_api_config(self):
        """Test APIConfig"""
        from polls.api_config import APIConfig, API_ENDPOINTS
        self.assertTrue(all(key in API_ENDPOINTS for key in [
            'addToInventory',
            'removeFromInventory',
            'addToShoppingList',
            'removeFromShoppingList',
            'purchaseItem'
        ]))
