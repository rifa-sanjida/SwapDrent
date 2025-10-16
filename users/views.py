from django.shortcuts import render, redirect, get_object_or_404  # Page rendering and navigation
from django.contrib import messages  # System for showing success/error messages to users
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash  # Authentication tools
from django.contrib.auth.decorators import login_required  # Require users to be logged in
from django.contrib.auth.models import User  # Built-in user model
from django.contrib.auth.forms import PasswordChangeForm  # Built-in password change form
from django.contrib.auth.tokens import default_token_generator  # Secure password reset tokens
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  # URL-safe encoding
from django.utils.encoding import force_bytes, force_str  # String encoding utilities
from django.template.loader import render_to_string  # Render HTML templates to strings
from django.core.mail import send_mail  # Email sending functionality
from django.conf import settings  # Access project settings
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, AccountDeleteForm, PasswordResetRequestForm, \
    SetNewPasswordForm  # Our custom forms


def register(request):
    """Handle new user registration - creating accounts"""
    if request.method == 'POST':  # If user submitted the registration form
        form = UserRegisterForm(request.POST)  # Create form with submitted data
        if form.is_valid():  # If all data is valid (username available, passwords match, etc.)
            user = form.save()  # Create the new user account
            login(request, user)  # Automatically log the user in after registration
            messages.success(request, 'Your account has been created! Welcome to SwapDonateRent!')  # Success message
            return redirect('core:home')  # Send them to homepage
    else:
        form = UserRegisterForm()  # Create empty form for first-time page load

    # Show registration form (with errors if any)
    return render(request, 'users/register.html', {'form': form})

