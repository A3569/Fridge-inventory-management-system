from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import ItemType, IndividualItems, ShoppingList

# Configure admin site
admin.site.site_header = "Fridge Management Admin"
admin.site.site_title = "Fridge Management Admin Portal"
admin.site.index_title = "Welcome to Fridge Management Portal"
admin.site.site_url = '/user/'

# Register your models
@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'unique_barcode', 'amount_type')
    search_fields = ('name', 'unique_barcode')

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True

@admin.register(IndividualItems)
class IndividualItemsAdmin(admin.ModelAdmin):
    list_display = ('item_type', 'amount', 'expiration_date')
    list_filter = ('item_type', 'expiration_date')
    search_fields = ('item_type__name',)

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True

@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('item_type', 'amount')
    list_filter = ('item_type',)
    search_fields = ('item_type__name',)

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True