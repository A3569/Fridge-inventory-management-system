from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import ItemType, IndividualItems, ShoppingList
import requests
import json
from django.views.decorators.csrf import csrf_exempt

API_BASE_URL = 'http://localhost:3000/api/v1'

def index(request):
    # Create or get the default user without staff privileges
    user, created = User.objects.get_or_create(
        username='default_user',
        defaults={
            'is_active': True,
            'is_staff': False,
            'password': ''
        }
    )
    
    # If user exists but has staff status, remove it
    if not created and user.is_staff:
        user.is_staff = False
        user.save()
    
    # Auto-login the user
    if not request.user.is_authenticated:
        user.backend = 'polls.auth.NoPasswordBackend'
        login(request, user)
    
    return render(request, "polls/index.html")

def add_to_inventory(request):
    item_types = ItemType.objects.all()
    return render(request, 'polls/add_to_inventory.html', {
        'item_types': item_types
    })

def shopping_list(request):
    shopping_items = ShoppingList.objects.select_related('item_type').all()
    item_types = ItemType.objects.all()
    
    return render(request, 'polls/shopping_list.html', {
        'shopping_items': shopping_items,
        'item_types': item_types
    })

def inventory_list(request):
    items = IndividualItems.objects.select_related('item_type').all()
    return render(request, 'polls/inventory_list.html', {
        'items': items
    })

def grid_view(request):
    items = IndividualItems.objects.select_related('item_type').all()
    return render(request, 'polls/grid_view.html', {
        'items': items
    })

@csrf_exempt
def api_add_to_inventory(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received data:", data)
            
            item_type = ItemType.objects.get(unique_barcode=data['itemType'])
            print("Found item type:", item_type)
            
            # Create the inventory item
            item = IndividualItems.objects.create(
                item_type=item_type,
                amount=data['amount'],
                expiration_date=data['expirationDate']
            )
            print("Created inventory item:", item)
            
            return JsonResponse({
                'message': 'Item added successfully',
                'item': {
                    'id': item.id,
                    'name': item.item_type.name,
                    'amount': item.amount,
                    'expiration_date': item.expiration_date
                }
            })
        except ItemType.DoesNotExist:
            print(f"ItemType not found for barcode: {data.get('itemType')}")
            return JsonResponse({'error': 'Item type not found'}, status=404)
        except KeyError as e:
            print(f"Missing required field: {e}")
            return JsonResponse({'error': f'Missing required field: {e}'}, status=400)
        except Exception as e:
            print(f"Error adding to inventory: {e}")
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def api_remove_from_inventory(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        try:
            item = IndividualItems.objects.get(id=data['itemId'])
            item.delete()
            return JsonResponse({'message': 'Item removed successfully'})
        except Exception as e:
            print(f"Error removing from inventory: {e}")
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=405)

def api_add_to_shopping_list(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            item_type = ItemType.objects.get(unique_barcode=data['itemType'])
            # Update or create shopping list item
            shopping_item, created = ShoppingList.objects.get_or_create(
                item_type=item_type,
                defaults={'amount': data['amount']}
            )
            if not created:
                shopping_item.amount += data['amount']
                shopping_item.save()
            return JsonResponse({'message': 'Item added successfully'})
        except Exception as e:
            print(f"Error adding to shopping list: {e}")
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=405)

def api_remove_from_shopping_list(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        try:
            item = ShoppingList.objects.get(item_type__unique_barcode=data['itemType'])
            item.delete()
            return JsonResponse({'message': 'Item removed successfully'})
        except Exception as e:
            print(f"Error removing from shopping list: {e}")
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=405)

def api_purchase_item(request):
    if request.method == 'PATCH':
        data = json.loads(request.body)
        try:
            item_type = ItemType.objects.get(unique_barcode=data['itemType'])
            # Add to inventory
            IndividualItems.objects.create(
                item_type=item_type,
                amount=data['amount'],
                expiration_date=data['expirationDate']
            )
            # Remove from shopping list
            ShoppingList.objects.filter(item_type=item_type).delete()
            return JsonResponse({'message': 'Item purchased successfully'})
        except Exception as e:
            print(f"Error purchasing item: {e}")
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=405)