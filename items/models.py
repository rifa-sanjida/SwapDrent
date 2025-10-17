from django.db import models  # Database tools
from django.contrib.auth.models import User  # User accounts
from core.models import Category  # Our category system


class Item(models.Model):
    """Represents an item that can be swapped, donated, or rented"""

    # Different types of transactions users can do
    ITEM_TYPES = [
        ('swap', 'Swap'),  # Trade item for another item
        ('donate', 'Donate'),  # Give item away for free
        ('rent', 'Rent'),  # Lend item for a fee
    ]

    # Condition descriptions to help buyers know what to expect
    CONDITION_CHOICES = [
        ('new', 'New'),  # Never used, with tags
        ('like_new', 'Like New'),  # Used but looks brand new
        ('good', 'Good'),  # Normal wear and tear
        ('fair', 'Fair'),  # Visible signs of use
        ('poor', 'Poor'),  # Heavily used but functional
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')  # Who owns this item
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='items')  # What category this belongs to
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES)  # swap, donate, or rent
    name = models.CharField(max_length=200)  # Title of the item listing
    description = models.TextField()  # Detailed description of the item
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Price for rent/sale items
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='good')  # Item condition
    location = models.CharField(max_length=200)  # Where the item is located
    contact_info = models.CharField(max_length=200)  # How to contact the owner
    image = models.ImageField(upload_to='items/')  # Photo of the item
    is_active = models.BooleanField(default=True)  # Whether this listing is still available
    created_at = models.DateTimeField(auto_now_add=True)  # When item was posted
    updated_at = models.DateTimeField(auto_now=True)  # When item was last edited

    def __str__(self):
        return f"{self.name} ({self.get_item_type_display()})"  # Show item name and type

    class Meta:
        ordering = ['-created_at']  # Show newest items first by default


class Conversation(models.Model):
    """A chat between users about a specific item"""
    participants = models.ManyToManyField(User, related_name='conversations')  # Users in this chat
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name='conversations')  # Which item they're discussing
    created_at = models.DateTimeField(auto_now_add=True)  # When conversation started
    updated_at = models.DateTimeField(auto_now=True)  # When last message was sent

    def __str__(self):
        return f"Conversation about {self.item.name}"  # Show which item this chat is about

    class Meta:
        ordering = ['-updated_at']  # Show most active conversations first


class Message(models.Model):
    """A single message in a conversation between users"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,
                                     related_name='messages')  # Which chat this belongs to
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')  # Who sent this message
    content = models.TextField()  # The actual message text
    is_read = models.BooleanField(default=False)  # Whether recipient has read this
    created_at = models.DateTimeField(auto_now_add=True)  # When message was sent

    def __str__(self):
        return f"Message from {self.sender.username}"  # Show who sent the message

    class Meta:
        ordering = ['created_at']  # Show messages in chronological order
