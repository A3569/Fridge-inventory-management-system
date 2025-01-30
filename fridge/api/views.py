from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..models import IndividualItem, ItemType, ShoppingList
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
import uuid

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def add_item(request):
    try:
        item_name = request.data.get('itemType')
        amount = request.data.get('amount')
        expiration_date = request.data.get('expirationDate')

        if not all([item_name, amount, expiration_date]):
            return Response({'error': 'Missing required fields'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
        except ValueError:
            return Response({'error': 'Invalid amount value'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        item_type = get_object_or_404(ItemType, user=request.user, name=item_name)

        IndividualItem.objects.create(
            user=request.user,
            item_type=item_type,
            amount=amount,
            expiration_date=expiration_date
        )

        # Try to remove from shopping list if it exists
        try:
            shopping_item = ShoppingList.objects.get(item_type=item_type)
            shopping_item.delete()
        except ShoppingList.DoesNotExist:
            pass  # Item wasn't in shopping list, that's fine

        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_item(request):
    try:
        item_id = request.data.get('ID')
        if not item_id:
            return Response({'error': 'ID is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        item = get_object_or_404(IndividualItem, id=item_id)
        item.delete()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_items(request):
    try:
        items = request.data
        if not items or not isinstance(items, list):
            return Response({'error': 'List of items is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        item_ids = [item.get('ID') for item in items if item.get('ID')]
        IndividualItem.objects.filter(id__in=item_ids).delete()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def new_type(request):
    try:
        name = request.data.get('name')
        category = request.data.get('category')
        amount_type = request.data.get('amount type')
        photo_url = request.data.get('photo_url')

        if not all([name, category, amount_type]):
            return Response({'error': 'Missing required fields'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # Use name as a unique identifier per user
        item_type, created = ItemType.objects.get_or_create(
            user=request.user,
            name=name,
            defaults={
                'category': category,
                'amount_type': amount_type,
                'barcode': str(uuid.uuid4()),
                'photo_url': photo_url
            }
        )
        
        if not created:
            item_type.category = category
            item_type.amount_type = amount_type
            if photo_url:
                item_type.photo_url = photo_url
            item_type.save()
            
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_type(request):
    try:
        barcode = request.data.get('unique barcode')
        if not barcode:
            return Response({'error': 'Barcode is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        item_type = get_object_or_404(ItemType, barcode=barcode)
        
        if IndividualItem.objects.filter(item_type=item_type).exists():
            return Response(
                {'error': 'Cannot delete type with existing items'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        item_type.delete()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def add_to_shopping_list(request):
    try:
        item_name = request.data.get('itemType')
        amount = request.data.get('amount')
        category = request.data.get('category', 'OTHER')
        amount_type = request.data.get('amount_type', 'pieces')

        if not all([item_name, amount]):
            return Response({'error': 'Missing required fields'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # First, try to find existing item type
        item_type = ItemType.objects.filter(user=request.user, name=item_name).first()
        
        # If item type doesn't exist, create it
        if not item_type:
            item_type = ItemType.objects.create(
                user=request.user,
                name=item_name,
                barcode=str(uuid.uuid4()),
                amount_type=amount_type,
                category=category
            )
        else:
            # Update existing item type with new category if provided
            if category != 'OTHER':
                item_type.category = category
                item_type.save()

        # Add to shopping list
        shopping_item, created = ShoppingList.objects.get_or_create(
            user=request.user,
            item_type=item_type,
            defaults={'amount': float(amount)}
        )

        if not created:
            shopping_item.amount = F('amount') + float(amount)
            shopping_item.save()
            shopping_item.refresh_from_db()

        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_shopping_list(request):
    try:
        item_name = request.data.get('itemType')
        if not item_name:
            return Response({'error': 'Item name is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        item_type = get_object_or_404(ItemType, user=request.user, name=item_name)
        shopping_item = get_object_or_404(ShoppingList, user=request.user, item_type=item_type)
        shopping_item.delete()

        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def purchase_item(request):
    try:
        item_type = get_object_or_404(ItemType, id=request.data.get('item type'))
        amount = request.data.get('amount')
        expiration_date = request.data.get('expiration date')

        if not all([amount, expiration_date]):
            return Response({'error': 'Missing required fields'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # Remove from shopping list
        shopping_item = get_object_or_404(ShoppingList, item_type=item_type)
        shopping_item.amount = F('amount') - amount
        shopping_item.save()
        
        shopping_item.refresh_from_db()
        if shopping_item.amount <= 0:
            shopping_item.delete()

        # Add to individual items
        IndividualItem.objects.create(
            user=request.user,
            item_type=item_type,
            amount=amount,
            expiration_date=expiration_date
        )

        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 