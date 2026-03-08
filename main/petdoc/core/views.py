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
