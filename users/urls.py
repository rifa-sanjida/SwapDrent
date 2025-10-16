from django.urls import path  # URL routing tool
from . import views  # Import all our user-related view functions

app_name = 'users'  # Namespace for user URLs

# All URLs related to user accounts start with /users/
urlpatterns = [
    path('register/', views.register, name='register'),  # Sign up page
    path('login/', views.user_login, name='login'),  # Log in page
    path('logout/', views.user_logout, name='logout'),  # Log out
    path('profile/', views.profile, name='profile'),  # Edit profile
    path('change-password/', views.change_password, name='change_password'),  # Change password
    path('delete-account/', views.delete_account, name='delete_account'),  # Delete account

    # Password reset flow - for when users forget passwords
    path('password-reset/', views.password_reset_request, name='password_reset_request'),  # Request reset
    path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    # Confirm reset
    path('password-reset-done/', views.password_reset_done, name='password_reset_done'),  # Reset complete
]
