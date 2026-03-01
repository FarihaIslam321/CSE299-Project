# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import RegisterForm 
from django.contrib.auth import get_user_model 
from django.db import IntegrityError 
from django.contrib.auth import logout# Import your form if you've created one


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Get cleaned data from the form
            full_name = form.cleaned_data['fullName']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            country = form.cleaned_data['country']

            try:
                # Create the user object with a unique username (email)
                user = get_user_model().objects.create_user(username=email, email=email, password=password)
                user.first_name = full_name  # Save the full name in first_name
                user.save()

                # Provide feedback to the user
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect('login')  # Redirect to login page

            except IntegrityError:
                # Handle the case when email already exists
                messages.error(request, "This email is already registered.")
                return render(request, 'register.html', {'form': form})

        else:
            # If form is not valid, show errors
            messages.error(request, "There was an error with your registration. Please try again.")
    
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

# User Login View
def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']  # Use email instead of username
        password = request.POST['password']
        
        # Authenticate the user using email instead of username
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page or any page you want after login
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'login.html')  # Re-render the login page with error message
    
    return render(request, 'login.html')

# Home Page View
def home(request):
    return render(request, 'index.html')


def user_logout(request):
    logout(request)
    return redirect('home') 