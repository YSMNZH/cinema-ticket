from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import CustomUser 
# users/views.py
from django.contrib.auth import login as auth_login  # Make sure to import it like this
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .forms import CustomUserLoginForm

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('profile')  # Redirect to your desired page after login
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'users/login.html')
    else:
        return render(request, 'users/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        name = request.POST['name']
        family_name = request.POST['family_name']
        date_birth = request.POST['date_birth']

        # Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        # Insert data into MySQL database
        try:
            user = CustomUser.objects.create(
                username=username,
                email=email,
                phone_number=phone_number,
                password=make_password(password),  # Hash the password before saving
                name=name,
                family_name=family_name,
                date_birth=date_birth
            )
            user.save()
            messages.success(request, "Registration successful!")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return render(request, 'register.html')

    return render(request, 'users/register.html')

def profile(request):
    return render(request, 'users/profile.html')