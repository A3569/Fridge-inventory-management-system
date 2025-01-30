from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),  # Make dashboard the home page
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('api/v1/', include('fridge.api.urls')),
    path('addToInventory', views.add_to_inventory, name='add_to_inventory'),
    path('shoppingList', views.shopping_list, name='shopping_list'),
    path('list/', views.inventory_list, name='inventory_list'),
    path('gridView/', views.grid_view, name='grid_view'),
    path('dashboard/', views.dashboard, name='dashboard'),
] 