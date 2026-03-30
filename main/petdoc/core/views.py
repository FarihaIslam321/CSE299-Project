from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from core.models import Product, Cart, CartItem, Wishlist


def home(request):
    return render(request, 'index.html')


def shop_page(request):
    products = Product.objects.select_related("category", "vendor").order_by("-created_at")

    cart_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_count = sum(item.quantity for item in cart.items.all())

    return render(request, 'shop.html', {
        'products': products,
        'cart_count': cart_count,
    })


def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "product-details.html", {"product": product})


@login_required(login_url='login')
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    subtotal = sum([item.get_total() for item in cart.items.all()])
    shipping = Decimal(str(request.session.get("shipping", "4.99")))

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
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    quantity = int(request.POST.get("quantity", 1))
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    cart_item.save()

    messages.success(request, f"{product.title} (x{quantity}) added to cart!")
    return redirect(request.META.get('HTTP_REFERER', 'shop_page'))


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
def update_shipping(request):
    if request.method == "POST":
        shipping = request.POST.get("shipping", "4.99")
        request.session["shipping"] = str(shipping)
        messages.success(request, "Shipping updated!")
    return redirect('cart_detail')


@login_required(login_url='login')
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.success(request, f"{product.title} removed from wishlist.")
    else:
        wishlist.products.add(product)
        messages.success(request, f"{product.title} added to wishlist.")

    return redirect(request.META.get('HTTP_REFERER', 'shop_page'))