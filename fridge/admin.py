from django.contrib import admin
from .models import ItemType, IndividualItem, ShoppingList

admin.site.register(ItemType)
admin.site.register(IndividualItem)
admin.site.register(ShoppingList) 