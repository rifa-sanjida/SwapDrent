from django.contrib import admin  # Django's admin interface
from .models import Category, Cart, CartItem  # Our custom models

@admin.register(Category)  # This makes Category model appear in admin panel
class CategoryAdmin(admin.ModelAdmin):
    """Customize how Categories appear in the admin dashboard"""
    list_display = ('name', 'created_at')  # Show these columns in the list view
    search_fields = ('name', 'description')  # Allow searching by name and description

@admin.register(Cart)  # Register Cart model in admin
class CartAdmin(admin.ModelAdmin):
    """Customize how Shopping Carts appear in admin"""
    list_display = ('user', 'created_at', 'total_items')  # Show user and item count
    # This shows how many items are in each cart in the admin list

@admin.register(CartItem)  # Register CartItem model in admin
class CartItemAdmin(admin.ModelAdmin):
    """Customize how items in carts appear in admin"""
    list_display = ('cart', 'item', 'quantity', 'added_at')  # Show cart, item, and quantity
    # This helps admins see what items users have saved in their carts
