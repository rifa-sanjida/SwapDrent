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
