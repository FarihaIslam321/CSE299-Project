from django.contrib import admin
from django.utils.html import format_html
from core.models import (
    Vendor, Category, Product,
    Cart, CartItem, Wishlist,
    Order, OrderItem, Review,
    Address,PaymentMethod
)

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
