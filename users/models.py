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
    def __str__(self):
        return f"{self.user.username}'s Profile"  # Show which user this profile belongs to

# These functions automatically create profiles when new users sign up
@receiver(post_save, sender=User)  # Run this after a User is saved
def create_user_profile(sender, instance, created, **kwargs):
    """When a new user account is created, automatically make a profile for them"""
    if created:  # Only for brand new users, not existing ones being updated
        Profile.objects.create(user=instance, full_name=instance.get_full_name() or instance.username)

@receiver(post_save, sender=User)  # Run this after a User is saved
def save_user_profile(sender, instance, **kwargs):
    """Whenever a user is saved, make sure their profile gets saved too"""
    instance.profile.save()  # Save the profile linked to this user
