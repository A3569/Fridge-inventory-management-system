from django.db import models

class ItemType(models.Model):
    """Model for different types of items that can be stored"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    unique_barcode = models.CharField(max_length=50, unique=True)
    amount_type = models.CharField(max_length=50)  # e.g., "pieces", "liters", etc.
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class IndividualItems(models.Model):
    """Model for actual items in inventory"""
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    amount = models.IntegerField()
    expiration_date = models.DateField()

    def __str__(self):
        return f"{self.item_type.name} ({self.amount})"

class ShoppingList(models.Model):
    """Model for items in shopping list"""
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    amount = models.IntegerField()