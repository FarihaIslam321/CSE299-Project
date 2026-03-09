from django.http import HttpResponse
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import (
    Vendor, Category, Product,
    Cart, CartItem, Wishlist,
    Order, OrderItem, Review
)


def home(request):
    return render(request, 'index.html')



def product_details(request, id):
    product = get_object_or_404(
        Product.objects.annotate(
            avg_rating=Avg("reviews__rating"),
            review_count=Count("reviews")
        ),
        id=id
    )

    return render(request, "product-details.html", {"product": product})


@login_required(login_url='login')
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Subtotal is already Decimal
    subtotal = sum([item.get_total() for item in cart.items.all()])

    # Get shipping from session (convert to Decimal)
    shipping = Decimal(str(request.session.get("shipping", "4.99")))

    # Auto free shipping if subtotal > 300
    if subtotal > Decimal("300"):
        shipping = Decimal("0")

    tax = (subtotal * Decimal("0.05")).quantize(Decimal("0.01"))
    discount = Decimal("0")

    grand_total = (subtotal + tax + shipping - discount).quantize(Decimal("0.01"))

    return render(request, 'cart_detail.html', {
        'cart': cart,
        'subtotal': subtotal,
        'tax': tax,
        'discount': discount,
        'shipping': shipping,
        'grand_total': grand_total,
    })

@login_required(login_url='login')
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart_detail')


@login_required(login_url='login')
def update_cart_quantity(request):
    if request.method == "POST":
        cart = Cart.objects.get(user=request.user)

        for item in cart.items.all():
            qty = request.POST.get(f"quantity_{item.id}")
            if qty:
                item.quantity = int(qty)
                item.save()

        messages.success(request, "Cart updated successfully!")

    return redirect('cart_detail')


@login_required(login_url='login')
def clear_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart.items.all().delete()
    messages.success(request, "Cart cleared.")
    return redirect('cart_detail')

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get quantity from POST, default = 1
    quantity = int(request.POST.get("quantity", 1))

    # Get existing cart item or create new
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity  # add to previous quantity

    cart_item.save()

    messages.success(request, f"{product.title} (x{quantity}) added to cart!")
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='login')
def update_shipping(request):
    if request.method == "POST":
        shipping = request.POST.get("shipping", "4.99")
        request.session["shipping"] = str(shipping)  # store as string for Decimal safety
        messages.success(request, "Shipping updated!")

    return redirect('cart_detail')