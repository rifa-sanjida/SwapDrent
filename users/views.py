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
def user_login(request):
    """Handle user login with username and password"""
    if request.method == 'POST':  # If user submitted login form
        username = request.POST['username']  # Get username from form
        password = request.POST['password']  # Get password from form
        user = authenticate(request, username=username, password=password)  # Verify credentials

        if user is not None:  # If username and password are correct
            login(request, user)  # Log the user in
            messages.success(request, f'Welcome back, {username}!')  # Personalized welcome
            return redirect('core:home')  # Send to homepage
        else:
            messages.error(request, 'Invalid username or password. Please try again.')  # Error message

    # Show login form (with error if login failed)
    return render(request, 'users/login.html')


def user_logout(request):
    """Handle user logout"""
    logout(request)  # End the user's session
    messages.success(request, 'You have been successfully logged out.')  # Confirmation message
    return redirect('core:home')  # Send to homepage


@login_required  # Only logged-in users can access this page
def profile(request):
    """Let users view and edit their profile information"""
    if request.method == 'POST':  # If user submitted profile changes
        u_form = UserUpdateForm(request.POST, instance=request.user)  # Update basic user info
        p_form = ProfileUpdateForm(request.POST, request.FILES,
                                   instance=request.user.profile)  # Update profile info + picture

        if u_form.is_valid() and p_form.is_valid():  # If both forms are valid
            u_form.save()  # Save user changes
            p_form.save()  # Save profile changes
            messages.success(request, 'Your profile has been updated successfully!')  # Success message
            return redirect('users:profile')  # Reload profile page
    else:
        # Pre-fill forms with current user data
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # Show profile editing page with current data
    return render(request, 'users/profile.html', {
        'u_form': u_form,  # User account form
        'p_form': p_form  # Profile information form
    })

