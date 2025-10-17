from django.contrib import admin
from .models import Item, Conversation, Message

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'item_type', 'category', 'price', 'is_active', 'created_at')
    list_filter = ('item_type', 'category', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'owner__username')

#ei ta mithila er code

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('item', 'created_at', 'updated_at')
    filter_horizontal = ('participants',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'conversation', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__username', 'conversation__item__name', 'content')
