from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from core.models import Product, Cart, CartItem, Wishlist
from .models import Appointment 
import os
from django.http import JsonResponse
from django.conf import settings
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import io
from PIL import Image


# 1. Import the NEW SDK
from google import genai
from google.genai import types

# 2. Configure the Client (Paste your actual API key here)
client = genai.Client(api_key="AIzaSyC6ZhqhIK2MS-Repc9jW7PdxQ2KhZad5yY")

# 3. Define the Professional AI Persona
system_instruction = (
    "You are an expert, empathetic virtual veterinarian assistant for the 'Smart Veterinary Care' platform. "
    "If the user says a casual greeting, introduce yourself warmly. "
    "If the user provides symptoms or an image of an animal, analyze it professionally. "
    "Provide potential causes, care advice, and ALWAYS conclude by clearly stating whether "
    "a physical vet visit is URGENT or if the owner should MONITOR the pet. "
    "Format your answers using Markdown (bolding, bullet points) for easy reading. "
    "Never prescribe exact medication dosages."
)




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


def appoint_page(request):
    doctors = [
        {
            "value": "dr_sarah",
            "name": "Dr. Sarah Ahmed",
            "specialty": "Pet Medicine Specialist",
            "details": "Expert in general pet health, fever, infection, digestive problems, and preventive care for cats and dogs.",
            "time": "Sat - Thu | 9:00 AM - 1:00 PM",
            "icon": "bi-heart-pulse"
        },
        {
            "value": "dr_rahim",
            "name": "Dr. Rahim Chowdhury",
            "specialty": "Veterinary Surgery Specialist",
            "details": "Specialized in minor and major surgeries, wound management, fracture care, and emergency procedures.",
            "time": "Sat - Wed | 3:00 PM - 8:00 PM",
            "icon": "bi-bandaid"
        },
        {
            "value": "dr_nabila",
            "name": "Dr. Nabila Islam",
            "specialty": "Skin & Allergy Specialist",
            "details": "Treats pet skin disease, hair loss, itching, fungal infections, and allergy-related conditions.",
            "time": "Sun - Thu | 10:00 AM - 2:00 PM",
            "icon": "bi-shield-plus"
        },
        {
            "value": "dr_tanvir",
            "name": "Dr. Tanvir Hossain",
            "specialty": "Bird & Exotic Pet Specialist",
            "details": "Focused on birds, rabbits, and exotic pets with special care, nutrition, and disease evaluation.",
            "time": "Mon - Thu | 4:00 PM - 7:00 PM",
            "icon": "bi-feather"
        },
        {
            "value": "dr_farzana",
            "name": "Dr. Farzana Kabir",
            "specialty": "Livestock Specialist",
            "details": "Experienced in cattle, goat, sheep, and farm animal treatment, vaccination, and herd health support.",
            "time": "Sat - Thu | 8:00 AM - 12:00 PM",
            "icon": "bi-house-heart"
        },
    ]
    return render(request, "appoint.html", {"doctors": doctors})


@require_POST
def submit_appointment(request):
    email = request.POST.get("email")
    doctor = request.POST.get("doctor")

    if not email or not doctor:
        messages.error(request, "Please provide your email and select a doctor.")
        return redirect("appoint_page")

    Appointment.objects.create(email=email, doctor=doctor)
    messages.success(request, "Appointment request submitted successfully. Our team will contact you soon.")
    return redirect("appoint_page")







def custom_vet_assistant(request):
    # Load the page
    if request.method == 'GET':
        return render(request, 'ai_chat.html') # Adjust path if your template is elsewhere

    # Handle the AI Request
    if request.method == 'POST':
        user_prompt = request.POST.get('prompt', '').strip()
        uploaded_image = request.FILES.get('image', None)

        if not user_prompt and not uploaded_image:
            return JsonResponse({'status': 'error', 'message': 'Please provide text or an image.'})

        try:
            prompt_parts = []
            
            # Add text
            if user_prompt:
                prompt_parts.append(user_prompt)
                
            # Add image
            if uploaded_image:
                image_bytes = uploaded_image.read()
                img = Image.open(io.BytesIO(image_bytes))
                prompt_parts.append(img)

            # Generate response using the NEW SDK and gemini-2.5-flash
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_parts,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                )
            )
            
            return JsonResponse({'status': 'success', 'reply': response.text})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f"AI Connection Error: {str(e)}"})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})