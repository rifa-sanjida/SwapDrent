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
@login_required  # Only logged-in users can change passwords
def change_password(request):
    """Let users change their password while logged in"""
    if request.method == 'POST':  # If user submitted password change form
        form = PasswordChangeForm(request.user, request.POST)  # Built-in password change form
        if form.is_valid():  # If current password is correct and new passwords match
            user = form.save()  # Update password
            update_session_auth_hash(request, user)  # Keep user logged in after password change
            messages.success(request, 'Your password has been changed successfully!')  # Success message
            return redirect('users:profile')  # Back to profile page
        else:
            messages.error(request, 'Please correct the errors below.')  # Show form errors
    else:
        form = PasswordChangeForm(request.user)  # Empty password change form

    # Show password change form
    return render(request, 'users/change_password.html', {'form': form})


@login_required  # Only logged-in users can delete accounts
def delete_account(request):
    """Let users permanently delete their account"""
    if request.method == 'POST':  # If user confirmed account deletion
        form = AccountDeleteForm(request.POST)  # Confirmation form
        if form.is_valid():  # If user checked the confirmation box
            request.user.delete()  # Permanently delete user account
            messages.success(request, 'Your account has been permanently deleted.')  # Confirmation
            return redirect('core:home')  # Send to homepage
    else:
        form = AccountDeleteForm()  # Empty confirmation form

    # Show account deletion confirmation page
    return render(request, 'users/delete_account.html', {'form': form})


def password_reset_request(request):
    """Handle requests to reset forgotten passwords"""
    if request.method == 'POST':  # If user submitted email for password reset
        form = PasswordResetRequestForm(request.POST)  # Email submission form
        if form.is_valid():  # If email is valid and registered
            email = form.cleaned_data['email']  # Get the email address
            associated_users = User.objects.filter(email=email)  # Find users with this email

            if associated_users.exists():  # If we found matching users
                for user in associated_users:
                    # Create secure reset token and encoded user ID
                    token = default_token_generator.make_token(user)  # One-time use token
                    uid = urlsafe_base64_encode(force_bytes(user.pk))  # Safe user ID for URL


                    reset_url = request.build_absolute_uri(
                        f'/users/password-reset-confirm/{uid}/{token}/'
                    )

                    # Create email content
                    subject = 'Reset Your Password - SwapDonateRent'
                    message = render_to_string('users/password_reset_email.html', {
                        'user': user,
                        'reset_url': reset_url,
                        'site_name': 'SwapDonateRent'
                    })

                    try:

                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            [email],
                            fail_silently=False,
                        )
                        messages.success(request, 'Password reset email sent! Check your inbox for instructions.')
                        return redirect('users:login')  # Back to login page
                    except Exception as e:
                        messages.error(request, 'Failed to send email. Please try again later.')
            else:
                messages.error(request, 'No account found with that email address.')
    else:
        form = PasswordResetRequestForm()  # Empty reset request form

    # Show password reset request form
    return render(request, 'users/password_reset_request.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
    """Let users set new password after clicking reset link"""
    try:
        # Decode the user ID from the URL
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)  # Find the user
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None  # Invalid user ID

 # Check if reset token is valid
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':  # If user submitted new password
            form = SetNewPasswordForm(user, request.POST)  # New password form
            if form.is_valid():  # If passwords are valid
                form.save()  # Save new password
                messages.success(request, 'Your password has been reset! You can now log in with your new password.')
                return redirect('users:login')  # Back to login
        else:
            form = SetNewPasswordForm(user)  # Empty new password form

        # Show form to set new password
        return render(request, 'users/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'Password reset link is invalid or has expired.')  # Invalid token
        return redirect('users:password_reset_request')  # Back to reset request


def password_reset_done(request):
    """Show confirmation that password reset was successful"""
    return render(request, 'users/password_reset_done.html')  # Simple confirmation page
