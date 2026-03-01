from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page or any page you want after login
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')  # Re-render the login page with error message
    
    return render(request, 'login.html')

def home(request):
    return render(request, 'index.html')