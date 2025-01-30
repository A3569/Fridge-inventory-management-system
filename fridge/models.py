from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    # Add custom fields if needed
    pass

class ItemType(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    CATEGORY_CHOICES = [
        ('DAIRY', 'Dairy Products'),
        ('MEAT', 'Meat & Poultry'),
        ('VEGETABLES', 'Vegetables'),
        ('FRUITS', 'Fruits'),
        ('GRAINS', 'Grains & Cereals'),
        ('BEVERAGES', 'Beverages'),
        ('SNACKS', 'Snacks'),
        ('FROZEN', 'Frozen Foods'),
        ('OTHER', 'Other'),
    ]

    barcode = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    amount_type = models.CharField(max_length=50)  # e.g., "pieces", "grams", "liters"
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='OTHER'
    )
    photo_url = models.URLField(blank=True, null=True)

    class Meta:
        unique_together = ['user', 'name']  # Make names unique per user

    def __str__(self):
        return self.name

class IndividualItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    amount = models.FloatField()
    expiration_date = models.DateField()

    def __str__(self):
        return f"{self.item_type.name} ({self.amount})"

class ShoppingList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.item_type.name} - {self.amount}" 