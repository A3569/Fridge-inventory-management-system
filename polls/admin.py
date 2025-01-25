from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import ItemType, IndividualItems, ShoppingList

# Configure admin site header and titles
admin.site.site_header = "Fridge Management Admin"
admin.site.site_title = "Fridge Management Admin Portal"
admin.site.index_title = "Welcome to Fridge Management Portal"
admin.site.site_url = '/user/'

# Register ItemType model with custom admin configuration
@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    # Configure display and search fields
    list_display = ('name', 'unique_barcode', 'amount_type')
    search_fields = ('name', 'unique_barcode')

    # Define permissions for admin actions
    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True

# Register IndividualItems model with custom admin configuration
@admin.register(IndividualItems)
class IndividualItemsAdmin(admin.ModelAdmin):
    list_display = ('item_type', 'amount', 'expiration_date')
    list_filter = ('item_type', 'expiration_date')
    search_fields = ('item_type__name',)

    # Define permissions for admin actions
    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True

# Register ShoppingList model with custom admin configuration
@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('item_type', 'amount')
    list_filter = ('item_type',)
    search_fields = ('item_type__name',)

    # Define permissions for admin actions
    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True