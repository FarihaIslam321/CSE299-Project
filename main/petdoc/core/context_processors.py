# core/context_processors.py
from django.db.models import Sum
from .models import Cart, Wishlist

def cart_item_count(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        count = cart.items.aggregate(total=Sum('quantity'))['total'] or 0
    else:
        count = 0
    return {'cart_item_count': count}


def wishlist_count(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        return {'wishlist': wishlist}
    return {'wishlist': None}