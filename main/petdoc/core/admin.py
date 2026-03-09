from django.contrib import admin
from django.utils.html import format_html
from core.models import (
    Vendor, Category, Product,
    Cart, CartItem, Wishlist,
    Order, OrderItem, Review,
    Address,PaymentMethod
)


# -------------------------
# Image thumbnail helper
# -------------------------
def get_image(obj):
    if obj.image:
        return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:5px;" />', obj.image.url)
    return "No Image"


# Vendor
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at", get_image)
    search_fields = ("name", "email")


# Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", get_image)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


# Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "vendor", "category", "price", "stock", "created_at", get_image)
    list_filter = ("category", "vendor")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


# Cart
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")


# Cart Items
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")


# Wishlist
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user",)
    filter_horizontal = ("products",)


# Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "status", "created_at")
    list_filter = ("status",)


# Order Item
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")


# Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_name', 'masked_number', 'is_default')

    
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'city', 'country', 'is_default')