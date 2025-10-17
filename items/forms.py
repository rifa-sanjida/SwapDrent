from django import forms  # Form handling
from .models import Item, Message  # Our item and message models

class ItemForm(forms.ModelForm):
    """Form for creating and editing item listings"""
    class Meta:
        model = Item  # This form works with Item model
        fields = ['category', 'item_type', 'name', 'description', 'price', 'condition', 'location', 'contact_info', 'image']  # All item fields
        widgets = {  # Customize how form fields look
            'description': forms.Textarea(attrs={
                'rows': 4,  # Make description box taller
                'placeholder': 'Describe your item... What makes it special?'  # Helpful hint
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Enter your city or neighborhood'  # Location hint
            }),
            'contact_info': forms.TextInput(attrs={
                'placeholder': 'Email or phone number for interested buyers'  # Contact hint
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': '0.00',  # Price format hint
                'step': '0.01'  # Allow decimal prices
            }),
        }

class MessageForm(forms.ModelForm):
    """Form for sending messages in conversations"""
    class Meta:
        model = Message  # This form works with Message model
        fields = ['content']  # Only the message text field
        widgets = {  # Customize the message input
            'content': forms.Textarea(attrs={
                'rows': 3,  # Reasonable height for chat
                'placeholder': 'Type your message here...',  # Chat hint
                'class': 'message-input'  # CSS class for styling
            }),
        }
