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
                return redirect("home")  # Change to login page URL if needed
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
