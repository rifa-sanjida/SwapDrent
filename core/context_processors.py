from .models import Cart, CartItem, Category  # Our database models
from items.models import Conversation, Message  # Messaging system models

def cart_count(request):
    """This makes the cart item count available on every page"""
    if request.user.is_authenticated:  # Only for logged-in users
        # Get the user's cart, or create one if it doesn't exist
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Count how many different items are in their cart
        count = CartItem.objects.filter(cart=cart).count()
    else:
        count = 0  # Guests don't have carts
    return {'cart_count': count}  # This number will be available in all templates
def categories(request):
    """This makes all categories available for the navigation menu"""
    categories = Category.objects.all()  # Get every category from database
    return {'categories': categories}  # Categories will be in every page's navigation

def unread_messages_count(request):
    """This shows how many unread messages a user has"""
    if request.user.is_authenticated:  # Only for logged-in users
        # Count messages where user is participant, message is unread, and not sent by user
        count = Message.objects.filter(
            conversation__participants=request.user,  # User is in conversation
            is_read=False  # Message hasn't been read yet
        ).exclude(sender=request.user).count()  # Don't count user's own messages
    else:
        count = 0  # Guests don't have messages
    return {'unread_messages_count': count}  # This count shows in the navigation
