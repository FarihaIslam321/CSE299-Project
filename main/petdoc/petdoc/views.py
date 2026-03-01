# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import RegistrationForm  # Import your form if you've created one

# User Registration View
def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create the user if the form is valid
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            country = form.cleaned_data['country']

            # Create the user object
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = full_name
            user.save()

            # Provide feedback to the user
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')  # Redirect to login page
            
        else:
            # If form is not valid, show errors
            messages.error(request, "There was an error with your registration. Please try again.")
    
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})


# User Login View
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


# Home Page View
def home(request):
    return render(request, 'index.html')