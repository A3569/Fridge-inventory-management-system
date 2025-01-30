from django.urls import path
from . import views

urlpatterns = [
    path('addItem', views.add_item, name='add_item'),
    path('removeItem', views.remove_item, name='remove_item'),
    path('removeItems', views.remove_items, name='remove_items'),
    path('newType', views.new_type, name='new_type'),
    path('removeType', views.remove_type, name='remove_type'),
    path('addToShoppingList', views.add_to_shopping_list, name='add_to_shopping_list'),
    path('removeFromShoppingList', views.remove_from_shopping_list, name='remove_from_shopping_list'),
    path('purchaseItem', views.purchase_item, name='purchase_item'),
] 