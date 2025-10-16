from django import forms  # Django's form handling tools
from django.contrib.auth.models import User  # Built-in user model
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm  # Pre-built forms
from django.contrib.auth import authenticate  # User verification
from django.core.validators import validate_email  # Email format checking
from .models import Profile  # Our extended user profile


class UserRegisterForm(UserCreationForm):
    """Form for new users to create an account"""
    email = forms.EmailField(required=True)  # Require email address
    full_name = forms.CharField(max_length=200, required=True)  # Require full name

    class Meta:
        model = User  # This form creates User objects
        fields = ['username', 'full_name', 'email', 'password1', 'password2']  # Form fields

    def clean_email(self):
        """Make sure email isn't already used by another user"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():  # Check if email already exists
            raise forms.ValidationError('This email is already registered.')  # Show error
        return email  # Return valid email
