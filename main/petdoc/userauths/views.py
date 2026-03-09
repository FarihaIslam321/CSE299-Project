from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from userauths.forms import RegisterForm ,AddressForm, ReviewForm, PaymentMethodForm
from django.contrib.auth import authenticate, login, logout
from core.models import (
    Vendor, Category, Product,
    Cart, CartItem, Wishlist,
    Order, OrderItem, Review,
    Address,PaymentMethod
)



User = get_user_model()


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered. Please use a different email.")
            else:
                # Create user but don't commit yet
                user = form.save(commit=False)
                user.is_staff = False        # ensure normal user
                user.is_superuser = False    # ensure normal user
                user.save()                  # save to DB
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect("login")  # Change to login page URL if needed
        else:
            # Collect and display all form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate user using email as username
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Check if user is admin/staff
            if user.is_staff or user.is_superuser:
                messages.error(request, "Admin users cannot log in here. Please use the admin panel.")
                return redirect("login")  # redirect back to login page

            # Normal user login
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, "login.html")



def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")   # redirect to login page (change if needed)


@login_required
def account(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    wishlist = Wishlist.objects.filter(user=user).first()
    reviews = Review.objects.filter(user=user)
    addresses = Address.objects.filter(user=user)
    payments = PaymentMethod.objects.filter(user=user)

    products_ordered = Product.objects.filter(orderitem__order__user=user).distinct()
    
    context = {
        'user': user,
        'orders': orders,
        'wishlist': wishlist,
        'reviews': reviews,
        'addresses': addresses,
        'payments': payments,
        'products_ordered': products_ordered,
    }
    return render(request, 'account.html', context)


@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # assign current logged-in user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('account')
    else:
        form = ReviewForm()
    
    return render(request, 'add_review.html', {'form': form})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    messages.success(request, 'Review deleted!')
    return redirect('account')


@login_required
def add_payment_method(request):
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user  # Assign logged-in user
            payment.save()
            messages.success(request, 'Payment method added successfully!')
            return redirect('account')
        else:
            # Optional: show errors if form is invalid
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PaymentMethodForm()
    return render(request, 'add_payment.html', {'form': form})

@login_required
def delete_payment_method(request, payment_id):
    payment = get_object_or_404(PaymentMethod, id=payment_id, user=request.user)
    payment.delete()
    messages.success(request, 'Payment method deleted!')
    return redirect('account')



@login_required
def remove_wishlist(request, product_id):
    """
    Remove a product from the user's wishlist.
    """
    if request.method != "POST":
        return redirect('account')

    wishlist = Wishlist.objects.filter(user=request.user).first()
    if not wishlist:
        messages.error(request, "Wishlist not found.")
        return redirect('account')

    product = get_object_or_404(Product, id=product_id)
    # remove product if exists in wishlist
    wishlist.products.remove(product)
    messages.success(request, f"Removed {product.title} from your wishlist.")
    return redirect('account') 


@login_required
def toggle_wishlist(request, product_id):
    if request.method != "POST":
        return redirect('home')  # redirect if not POST

    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.success(request, f"Removed {product.title} from your wishlist.")
    else:
        wishlist.products.add(product)
        messages.success(request, f"Added {product.title} to your wishlist.")

    # Redirect back to the same page
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('account')
    else:
        form = RegisterForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user  # Assign the logged-in user
            address.save()
            messages.success(request, 'Address added successfully!')
            return redirect('account')
    else:
        form = AddressForm()
    return render(request, 'add_address.html', {'form': form})

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()  # Saves the existing instance
            messages.success(request, 'Address updated successfully!')
            return redirect('account')
    else:
        form = AddressForm(instance=address)
    return render(request, 'edit_address.html', {'form': form})

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted!')
    return redirect('account')


@login_required
def checkout(request):

    # Get user cart
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None

    cart_items = cart.items.all() if cart else []

    # Calculate totals
    subtotal = sum(item.get_total() for item in cart_items)  # subtotal is Decimal
    shipping = Decimal(request.session.get("shipping", 0))
    tax = subtotal * Decimal("0.05")   # FIXED
    discount = Decimal("0")
    grand_total = subtotal + shipping + tax - discount

    # Get Default Address
    default_address = Address.objects.filter(user=request.user, is_default=True).first()

    context = {
        "cart": cart,
        "cart_items": cart_items,
        "subtotal": subtotal,
        "tax": tax,
        "shipping": shipping,
        "discount": discount,
        "grand_total": grand_total,
        "default_address": default_address,
    }

    if request.session.get('buy_now'):
        del request.session['buy_now']
        

    return render(request, "checkout.html", context)


@login_required
def place_order(request):
    if request.method == "POST":
        cart = Cart.objects.filter(user=request.user).first()

        if not cart or not cart.items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect("checkout")

        # Get user's default address
        default_address = Address.objects.filter(user=request.user, is_default=True).first()
        if not default_address:
            messages.error(request, "Please add a default shipping address.")
            return redirect("checkout")

        # Totals
        subtotal = sum(item.get_total() for item in cart.items.all())
        shipping = Decimal(request.session.get("shipping", 0))
        tax = subtotal * Decimal("0.05")
        discount = Decimal("0")
        grand_total = subtotal + shipping + tax - discount

        # Create order (must match your model fields!)
        order = Order.objects.create(
            user=request.user,
            total_amount=grand_total,
        )

        # Create order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        # Empty cart
        cart.items.all().delete()

        messages.success(request, "🎉 Your order has been placed successfully!")
        return redirect("order_success")

    return redirect("checkout")


def order_success(request):
    return render(request, "order_success.html")


@login_required(login_url='login')
def buy_now(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get("quantity", 1))

        # Get or create cart
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Add product to cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

        # Store flag in session to go directly to checkout
        request.session['buy_now'] = True

        return redirect('checkout')
    else:
        return redirect(request.META.get('HTTP_REFERER', 'home'))