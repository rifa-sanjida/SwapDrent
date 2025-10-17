from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Item, Conversation, Message
from .forms import ItemForm, MessageForm
from core.models import Cart, CartItem


def item_list(request):
    items = Item.objects.filter(is_active=True)
    item_type = request.GET.get('type', '')
    category_id = request.GET.get('category', '')
    sort = request.GET.get('sort', '')
    search_query = request.GET.get('search', '')

    # Filter by type
    if item_type:
        items = items.filter(item_type=item_type)

    # Filter by category
    if category_id:
        items = items.filter(category_id=category_id)

    # Search by name or description
    if search_query:
        items = items.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Sort items
    if sort == 'price_low_high':
        items = items.order_by('price')
    elif sort == 'price_high_low':
        items = items.order_by('-price')
    elif sort == 'newest':
        items = items.order_by('-created_at')
    elif sort == 'oldest':
        items = items.order_by('created_at')
    else:
        items = items.order_by('-created_at')

    return render(request, 'items/item_list.html', {'items': items})


def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk, is_active=True)
    return render(request, 'items/item_detail.html', {'item': item})


@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, 'Item posted successfully!')
            return redirect('items:item_detail', pk=item.pk)
    else:
        form = ItemForm()
    return render(request, 'items/item_form.html', {'form': form, 'title': 'Post New Item'})


@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('items:item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'items/item_form.html', {'form': form, 'title': 'Edit Item'})


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('users:profile')
    return render(request, 'items/item_confirm_delete.html', {'item': item})


@login_required
def my_items(request):
    items = Item.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'items/my_items.html', {'items': items})


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk, is_active=True)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'{item.name} added to cart!')
    return redirect('items:cart')


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'items/cart.html', {'cart_items': cart_items})


@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('items:cart')


#for mithila


@login_required
def conversations_list(request):
    conversations = Conversation.objects.filter(participants=request.user).order_by('-updated_at')

    # Add unread counts to each conversation
    for conversation in conversations:
        # Calculate unread messages for this conversation
        unread_count = Message.objects.filter(
            conversation=conversation,
            is_read=False
        ).exclude(sender=request.user).count()

        # Add as attribute to the conversation object
        conversation.unread_count = unread_count

    return render(request, 'items/conversations.html', {'conversations': conversations})


@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()

            conversation.save()  # Update updated_at

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': {
                        'content': message.content,
                        'sender': message.sender.username,
                        'created_at': message.created_at.strftime('%b %d, %Y %H:%M'),
                        'is_own': True
                    }
                })
            return redirect('items:conversation_detail', conversation_id=conversation_id)
    else:
        form = MessageForm()

    # Mark messages as read when user views the conversation
    unread_messages = conversation.messages.filter(is_read=False).exclude(sender=request.user)
    unread_messages.update(is_read=True)

    # Get the other user in the conversation
    other_user = conversation.participants.exclude(id=request.user.id).first()

    return render(request, 'items/conversation_detail.html', {
        'conversation': conversation,
        'form': form,
        'other_user': other_user
    })


@login_required
def start_conversation(request, item_id):
    item = get_object_or_404(Item, id=item_id, is_active=True)

    if request.user == item.owner:
        messages.error(request, "You cannot start a conversation about your own item.")
        return redirect('items:item_detail', pk=item_id)

    # Check if conversation already exists
    conversation = Conversation.objects.filter(
        participants=request.user,
        item=item
    ).first()

    if not conversation:
        conversation = Conversation.objects.create(item=item)
        conversation.participants.add(request.user, item.owner)
        messages.success(request, f"Conversation started with {item.owner.username} about '{item.name}'")
    else:
        messages.info(request, f"Continuing conversation with {item.owner.username} about '{item.name}'")

    return redirect('items:conversation_detail', conversation_id=conversation.id)


@login_required
def get_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    messages_list = conversation.messages.all().order_by('created_at')

    messages_data = []
    for msg in messages_list:
        messages_data.append({
            'content': msg.content,
            'sender': msg.sender.username,
            'created_at': msg.created_at.strftime('%b %d, %Y %H:%M'),
            'is_own': msg.sender == request.user
        })

    return JsonResponse({'messages': messages_data})


# Additional utility view to mark a single message as read
@login_required
def mark_message_read(request, message_id):
    message = get_object_or_404(Message, id=message_id, conversation__participants=request.user)
    if message.sender != request.user:  # Only mark others' messages as read
        message.is_read = True
        message.save()

    return JsonResponse({'success': True})


# View to delete a conversation
@login_required
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)

    if request.method == 'POST':
        conversation.delete()
        messages.success(request, 'Conversation deleted successfully!')
        return redirect('items:conversations')

    return render(request, 'items/conversation_confirm_delete.html', {'conversation': conversation})
