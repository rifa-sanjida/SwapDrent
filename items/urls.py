from django.urls import path  # URL routing
from . import views  # Import all item-related view functions

app_name = 'items'  # Namespace for item URLs

# All URLs for items, cart, and messaging start with /items/
urlpatterns = [
    # Item browsing and management
    path('', views.item_list, name='item_list'),  # Browse all items
    path('my-items/', views.my_items, name='my_items'),  # View user's own items
    path('create/', views.item_create, name='item_create'),  # Post new item
    path('<int:pk>/', views.item_detail, name='item_detail'),  # View item details
    path('<int:pk>/edit/', views.item_update, name='item_update'),  # Edit existing item
    path('<int:pk>/delete/', views.item_delete, name='item_delete'),  # Delete item

    # Shopping cart functionality
    path('cart/', views.cart_view, name='cart'),  # View cart
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),  # Add item to cart
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),  # Remove from cart

    # Messaging system
    path('conversations/', views.conversations_list, name='conversations'),  # List conversations
    path('conversations/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    # View conversation
    path('conversations/<int:conversation_id>/messages/', views.get_messages, name='get_messages'),
    # AJAX: get messages
    path('conversations/start/<int:item_id>/', views.start_conversation, name='start_conversation'),  # Start new chat
    path('messages/<int:message_id>/read/', views.mark_message_read, name='mark_message_read'),  # Mark message as read
    path('conversations/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    # Delete conversation
]
