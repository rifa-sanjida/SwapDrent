from django.shortcuts import render  # Tool for rendering HTML pages
from items.models import Item  # Import our Item model to display items


def home(request):
    """This is the main homepage that visitors see first"""
    # Get the 8 most recently added active items to feature on homepage
    featured_items = Item.objects.filter(is_active=True).order_by('-created_at')[:8]

    # Render the homepage template and pass the featured items to it
    return render(request, 'core/home.html', {
        'featured_items': featured_items  # Send items to the template
    })


def about(request):
    """Simple about page that explains what our website does"""
    # Just render the about page template - no special data needed
    return render(request, 'core/about.html')


def contact(request):
    """Contact page where users can find how to reach us"""
    # Render the contact page template
    return render(request, 'core/contact.html')
