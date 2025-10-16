from django.db import models  # Django's database tools
from django.contrib.auth.models import User  # Built-in user accounts


class Category(models.Model):
    """Categories help organize items - like Electronics, Furniture, Books etc."""
    name = models.CharField(max_length=100)  # Category name like "Electronics"
    description = models.TextField(blank=True)  # Optional description of the category
    image = models.ImageField(upload_to='categories/', blank=True, null=True)  # Picture for the category
    created_at = models.DateTimeField(auto_now_add=True)  # When this category was created

    class Meta:
        verbose_name_plural = "Categories"  # Fixes Django's automatic "Categorys" to "Categories"

    def __str__(self):
        return self.name  # Show the category name in admin panel


class Cart(models.Model):
    """Each user has a shopping cart to save items they're interested in"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Which user owns this cart
    created_at = models.DateTimeField(auto_now_add=True)  # When the cart was created
    updated_at = models.DateTimeField(auto_now=True)  # When cart was last modified

    def __str__(self):
        return f"Cart of {self.user.username}"  # Show whose cart this is

    def total_items(self):
        """Count how many different items are in this cart"""
        return self.cartitem_set.count()


class CartItem(models.Model):
    """Represents one item added to a shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # Which cart this item belongs to
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE)  # The actual item being saved
    quantity = models.PositiveIntegerField(default=1)  # How many of this item (usually 1)
    added_at = models.DateTimeField(auto_now_add=True)  # When this item was added to cart

    class Meta:
        unique_together = ['cart', 'item']  # Prevent same item being added twice to same cart

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"  # Show item name and quantity
