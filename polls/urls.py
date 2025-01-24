from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path('addToInventory/', views.add_to_inventory, name='add_to_inventory'),
    path('shoppingList/', views.shopping_list, name='shopping_list'),
    path('list/', views.inventory_list, name='inventory_list'),
    path('grid_view/', views.grid_view, name='grid_view'),
    # API endpoints
    path('api/v1/addToInventory', views.api_add_to_inventory, name='api_add_to_inventory'),
    path('api/v1/removeFromInventory', views.api_remove_from_inventory, name='api_remove_from_inventory'),
    path('api/v1/addToShoppingList', views.api_add_to_shopping_list, name='api_add_to_shopping_list'),
    path('api/v1/removeFromShoppingList', views.api_remove_from_shopping_list, name='api_remove_from_shopping_list'),
    path('api/v1/purchaseItem', views.api_purchase_item, name='api_purchase_item'),
]