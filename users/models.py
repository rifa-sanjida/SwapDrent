from django.db import models  # Database tools
from django.contrib.auth.models import User  # Built-in user system
from django.db.models.signals import post_save  # Hook into when users are saved
from django.dispatch import receiver  # Connect functions to events

class Profile(models.Model):
    """Extra information about users beyond the basic account details"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to main user account
    full_name = models.CharField(max_length=200)  # User's full name for display
    phone = models.CharField(max_length=20, blank=True)  # Optional phone number
    address = models.TextField(blank=True)  # Optional home address
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)  # User's photo
    bio = models.TextField(blank=True)  # Optional "about me" description
    created_at = models.DateTimeField(auto_now_add=True)  # When profile was created
    updated_at = models.DateTimeField(auto_now=True)  # When profile was last updated
