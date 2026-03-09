from django.urls import path
from userauths import views


urlpatterns = [
    
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account, name='account'),
    path('account/edit/', views.edit_profile, name='edit_profile'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('payment/add/', views.add_payment_method, name='add_payment'),
    path('payment/delete/<int:payment_id>/', views.delete_payment_method, name='delete_payment'),
    path('wishlist/remove/<int:product_id>/', views.remove_wishlist, name='remove_wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('review/add/', views.add_review, name='add_review'),
    path('address/add/', views.add_address, name='add_address'),
    path('address/edit/<int:address_id>/', views.edit_address, name='edit_address'),
    path('address/delete/<int:address_id>/', views.delete_address, name='delete_address'),
    path("checkout/", views.checkout, name="checkout"),
    path("place-order/", views.place_order, name="place_order"),
    path("order-success/", views.order_success, name="order_success"),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),

]