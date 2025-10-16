from django.urls import path  # Tool for creating URL patterns
from . import views  # Import the view functions we just created

app_name = 'core'  # This helps organize URLs when we have multiple apps

# This list connects URLs to our view functions
urlpatterns = [
    path('', views.home, name='home'),      # Homepage at website root (/)
    path('about/', views.about, name='about'),    # About page at /about/
    path('contact/', views.contact, name='contact'), # Contact page at /contact/
]
