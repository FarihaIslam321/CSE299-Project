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
