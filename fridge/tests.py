from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from fridge.models import ItemType, IndividualItem, ShoppingList
from datetime import datetime, timedelta
import json

class FridgeTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

        # Create test item type
        self.item_type = ItemType.objects.create(
            user=self.user,
            name='Test Item',
            barcode='123456789',
            amount_type='pieces',
            category='OTHER'
        )

    def test_user_registration(self):
        """Test user registration functionality"""
        # First logout the current user
        self.client.logout()
        
        # Make the registration request
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        }, follow=True)
        
        # Debug prints
        print("Response status code:", response.status_code)
        if hasattr(response, 'context') and 'form' in response.context:
            print("Form errors:", response.context['form'].errors)
        print("Response redirect chain:", response.redirect_chain)
        
        # Check if user was created
        self.assertTrue(self.User.objects.filter(username='newuser').exists())
        
        # Check if user can login
        login_successful = self.client.login(username='newuser', password='TestPass123!')
        self.assertTrue(login_successful)
        
        # Check if redirected to home page
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)

    def test_add_item(self):
        """Test adding an item to inventory"""
        response = self.client.put(
            reverse('add_item'),
            json.dumps({
                'itemType': 'Test Item',
                'amount': 1,
                'expirationDate': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%d')
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(IndividualItem.objects.filter(item_type=self.item_type).exists())

    def test_remove_item(self):
        """Test removing an item from inventory"""
        # First create an item
        item = IndividualItem.objects.create(
            user=self.user,
            item_type=self.item_type,
            amount=1,
            expiration_date=timezone.now() + timedelta(days=7)
        )

        response = self.client.delete(
            reverse('remove_item'),
            json.dumps({'ID': str(item.id)}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(IndividualItem.objects.filter(id=item.id).exists())

    def test_add_to_shopping_list(self):
        """Test adding an item to shopping list"""
        response = self.client.put(
            reverse('add_to_shopping_list'),
            json.dumps({
                'itemType': 'Test Item',
                'amount': 2
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ShoppingList.objects.filter(item_type=self.item_type).exists())

    def test_remove_from_shopping_list(self):
        """Test removing an item from shopping list"""
        # First add item to shopping list
        ShoppingList.objects.create(
            user=self.user,
            item_type=self.item_type,
            amount=2
        )

        response = self.client.delete(
            reverse('remove_from_shopping_list'),
            json.dumps({'itemType': 'Test Item'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ShoppingList.objects.filter(item_type=self.item_type).exists())

    def test_new_type(self):
        """Test creating a new item type"""
        response = self.client.put(
            reverse('new_type'),
            json.dumps({
                'name': 'New Test Item',
                'category': 'DAIRY',
                'amount type': 'liters'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ItemType.objects.filter(name='New Test Item').exists())

    def test_remove_type(self):
        """Test removing an item type"""
        response = self.client.delete(
            reverse('remove_type'),
            json.dumps({'unique barcode': '123456789'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ItemType.objects.filter(barcode='123456789').exists())

    def test_purchase_item(self):
        """Test purchasing an item from shopping list"""
        # Add item to shopping list first
        shopping_item = ShoppingList.objects.create(
            user=self.user,
            item_type=self.item_type,
            amount=2
        )

        response = self.client.patch(
            reverse('purchase_item'),
            json.dumps({
                'item type': self.item_type.id,
                'amount': 1,
                'expiration date': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%d')
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(IndividualItem.objects.filter(item_type=self.item_type).exists())
        shopping_item.refresh_from_db()
        self.assertEqual(shopping_item.amount, 1)

    def test_views_require_login(self):
        """Test that views require login"""
        self.client.logout()
        views_to_test = ['home', 'inventory_list', 'grid_view', 'shopping_list', 'add_to_inventory']
        
        for view_name in views_to_test:
            response = self.client.get(reverse(view_name))
            self.assertIn(response.status_code, [302, 403])  # Either redirect to login or forbidden

    def test_dashboard_statistics(self):
        """Test dashboard statistics calculation"""
        # Create some test data
        IndividualItem.objects.create(
            user=self.user,
            item_type=self.item_type,
            amount=1,
            expiration_date=timezone.now() + timedelta(days=3)
        )
        ShoppingList.objects.create(
            user=self.user,
            item_type=self.item_type,
            amount=2
        )

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fridge/dashboard.html')
        self.assertIn('total_inventory_items', response.context)
        self.assertIn('total_shopping_list_items', response.context)
        self.assertIn('expiring_soon', response.context)

    def test_manage_command(self):
        """Test Django's manage.py functionality"""
        from django.core.management import call_command
        from io import StringIO
        
        # Test check command instead of help
        out = StringIO()
        call_command('check', stdout=out)
        self.assertIn('System check identified no issues', out.getvalue())

class ItemTypeModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_item_type_creation(self):
        """Test ItemType model creation and string representation"""
        item_type = ItemType.objects.create(
            user=self.user,
            name='Test Item',
            barcode='123456789',
            amount_type='pieces',
            category='OTHER'
        )
        self.assertEqual(str(item_type), 'Test Item')
        self.assertEqual(item_type.category, 'OTHER')

class IndividualItemModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.item_type = ItemType.objects.create(
            user=self.user,
            name='Test Item',
            barcode='123456789',
            amount_type='pieces',
            category='OTHER'
        )

    def test_individual_item_creation(self):
        """Test IndividualItem model creation and string representation"""
        item = IndividualItem.objects.create(
            user=self.user,
            item_type=self.item_type,
            amount=1,
            expiration_date=timezone.now().date()
        )
        self.assertEqual(str(item), 'Test Item (1)')

class ShoppingListModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.item_type = ItemType.objects.create(
            user=self.user,
            name='Test Item',
            barcode='123456789',
            amount_type='pieces',
            category='OTHER'
        )

    def test_shopping_list_creation(self):
        """Test ShoppingList model creation and string representation"""
        shopping_item = ShoppingList.objects.create(
            user=self.user,
            item_type=self.item_type,
            amount=2
        )
        self.assertEqual(str(shopping_item), 'Test Item - 2') 