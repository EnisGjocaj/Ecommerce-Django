from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from conversation.models import Conversation

from item.models import Item
from dashboard.models import Cart
# @login_required
# def index(request):
# 	items = Item.objects.filter(created_by=request.user)

# 	return render(request, 'dashboard/index.html', {
# 		'items': items,
# 	})

@login_required
def index(request):
    # Get items in conversations initiated by the user
    items_in_conversations = Item.objects.filter(conversation__members=request.user)

    # Get items in the user's cart
    try:
        cart = Cart.objects.get(user=request.user)
        items_in_cart = cart.items.all()
    except Cart.DoesNotExist:
        items_in_cart = Item.objects.none()  # Create an empty queryset

    # Combine items from conversations and cart
    items = items_in_conversations | items_in_cart

    return render(request, 'dashboard/index.html', {
        'items': items.distinct(),
    })