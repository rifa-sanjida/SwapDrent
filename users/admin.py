from django.contrib import admin  # Admin interface
from .models import Profile  # Our custom user profile model

@admin.register(Profile)  # Make Profile model editable in admin
class ProfileAdmin(admin.ModelAdmin):
    """Customize how user profiles appear in admin panel"""
    list_display = ('user', 'full_name', 'phone')  # Show these columns
    search_fields = ('user__username', 'full_name', 'phone')  # Search by username, name, or phone
    # This helps admins find specific users and their profile information
