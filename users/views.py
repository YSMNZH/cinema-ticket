
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import User  # Assuming you have a custom User model
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import RegistrationForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']

            # Determine if identifier is email, phone, or username
            if '@' in identifier:
                user = authenticate(request, email=identifier, password=password)
            elif identifier.isdigit():
                user = authenticate(request, phone=identifier, password=password)
            else:
                user = authenticate(request, username=identifier, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # Change 'home' to your target page
            else:
                form.add_error(None, "Invalid credentials or verification needed.")
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('home')  # Redirect to a home page or user dashboard after registration
    else:
        form = RegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})
