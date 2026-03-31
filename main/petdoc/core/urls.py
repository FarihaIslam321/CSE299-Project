from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop_page, name='shop_page'),
    path("product/<int:id>/", views.product_details, name="product_details"),

    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('cart/update/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/update-shipping/', views.update_shipping, name='update_shipping'),
    path('appointment/', views.appoint_page, name='appoint_page'),
    path('appointment/submit/', views.submit_appointment, name='submit_appointment'),

    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)