from django.shortcuts import render, redirect
from .models import ItemType, ShoppingList, IndividualItem
from django.utils import timezone
from django.db.models import Count, Sum
from itertools import groupby
from operator import attrgetter
from django.db.models.functions import ExtractMonth
from datetime import timedelta
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm

def add_to_inventory(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get parameters from URL if they exist
    context = {
        'categories': ItemType.CATEGORY_CHOICES,
        'today': timezone.now().date(),
        'prefill': {
            'itemName': request.GET.get('itemName', ''),
            'category': request.GET.get('category', ''),
            'amount': request.GET.get('amount', ''),
            'amountType': request.GET.get('amountType', 'pieces'),
        }
    }
    return render(request, 'fridge/add_to_inventory.html', context)

def shopping_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Filter by current user
    shopping_items = ShoppingList.objects.select_related('item_type').filter(
        user=request.user
    )
    item_types = ItemType.objects.filter(user=request.user).order_by('name')
    
    context = {
        'shopping_items': shopping_items,
        'item_types': item_types,
        'categories': ItemType.CATEGORY_CHOICES,
        'today': timezone.now().date(),
    }
    return render(request, 'fridge/shopping_list.html', context)

def inventory_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Filter by current user
    inventory_items = IndividualItem.objects.select_related('item_type').filter(
        user=request.user
    ).order_by('item_type__category', 'expiration_date')
    
    # Group items by category
    grouped_items = {}
    for category, items in groupby(inventory_items, key=lambda x: x.item_type.get_category_display()):
        grouped_items[category] = list(items)
    
    context = {
        'grouped_items': grouped_items,
        'categories': ItemType.CATEGORY_CHOICES,
    }
    return render(request, 'fridge/inventory_list.html', context)

def grid_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Filter by current user
    inventory_items = IndividualItem.objects.select_related('item_type').filter(
        user=request.user
    ).order_by('item_type__category', 'item_type__name')
    
    grouped_items = {}
    for category, items in groupby(inventory_items, key=lambda x: x.item_type.get_category_display()):
        grouped_items[category] = list(items)
    
    context = {
        'grouped_items': grouped_items,
        'categories': ItemType.CATEGORY_CHOICES,
        'placeholder_image': 'https://placehold.co/600x400/png?text=No+Image'
    }
    return render(request, 'fridge/grid_view.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print("Form errors:", form.errors)
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    # Get basic statistics
    total_inventory_items = IndividualItem.objects.filter(user=request.user).count()
    total_shopping_list_items = ShoppingList.objects.filter(user=request.user).count()
    unique_item_types = ItemType.objects.filter(user=request.user).count()
    
    # Get items expiring soon (within 7 days)
    today = timezone.now().date()
    week_later = today + timedelta(days=7)
    expiring_soon = IndividualItem.objects.filter(
        user=request.user,
        expiration_date__range=[today, week_later]
    ).count()

    # Get inventory by category
    inventory_by_category = (
        IndividualItem.objects
        .filter(user=request.user)
        .values('item_type__category')
        .annotate(count=Count('id'))
        .order_by('item_type__category')
    )

    # Get shopping list by category
    shopping_by_category = (
        ShoppingList.objects
        .filter(user=request.user)
        .values('item_type__category')
        .annotate(count=Count('id'))
        .order_by('item_type__category')
    )

    # Get items by expiration month
    items_by_expiration = (
        IndividualItem.objects
        .filter(user=request.user)
        .annotate(month=ExtractMonth('expiration_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Get low stock items (less than 2 units)
    low_stock_items = (
        IndividualItem.objects
        .filter(user=request.user)
        .values('item_type__name')
        .annotate(total_amount=Sum('amount'))
        .filter(total_amount__lt=2)
        .order_by('item_type__name')
    )[:5]  # Top 5 low stock items

    context = {
        'total_inventory_items': total_inventory_items,
        'total_shopping_list_items': total_shopping_list_items,
        'unique_item_types': unique_item_types,
        'expiring_soon': expiring_soon,
        'inventory_by_category': list(inventory_by_category),
        'shopping_by_category': list(shopping_by_category),
        'items_by_expiration': list(items_by_expiration),
        'low_stock_items': list(low_stock_items),
        'categories': dict(ItemType.CATEGORY_CHOICES),
    }
    return render(request, 'fridge/dashboard.html', context) 