from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password 
from .models import User
from .forms import LoginForm
from .forms import RegistrationForm
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data.get("identifier")
            password = form.cleaned_data.get("password")
            user = (
                User.objects.filter(phone=identifier).first() or
                User.objects.filter(email=identifier).first() or
                User.objects.filter(username=identifier).first()
            )

            if user and check_password(password, user.password):

                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Invalid Login Credentials. Please Try Again.")

    else:
        form = LoginForm()

    return render(request, 'users/login.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth import login
from .models import User

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the user to the database
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Log the user in automatically after registration
            messages.success(request, "You have registered successfully!")
            return redirect("dashboard")  # Redirect to the dashboard
        else:
            # If the form is invalid, display the errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistrationForm()
    
    return render(request, "users/register.html", {"form": form})


from django.shortcuts import render

def main_view(request):
    return render(request, 'users/main.html')

def edit_view(request):
    return render(request, 'users/edit.html')
