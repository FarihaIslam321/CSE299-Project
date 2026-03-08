from django.urls import path
from userauths import views


urlpatterns = [
    
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
     path('account/', views.account, name='account'),
    path('account/edit/', views.edit_profile, name='edit_profile'),
]