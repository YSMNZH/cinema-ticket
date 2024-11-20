from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import CustomUser 
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.utils.crypto import get_random_string
from .forms import RegisterForm
from django.shortcuts import render
from .models import CustomUser, PasswordResetToken
from django.core.mail import send_mail




def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('profile') 
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'users/login.html')
        
    return render(request, 'users/login.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.password = make_password(form.cleaned_data['password'])
                user.save()

                messages.success(request, "Registration successful!")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")

    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

def profile(request):
    return render(request, 'users/profile.html')

def request_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            token = get_random_string(64)
            PasswordResetToken.objects.create(user=user, token=token)

            reset_link = f"http://127.0.0.1:8000/users/reset-password/{token}/"

            subject = "Password Reset Request"
            message = f"Click the link below to reset your password:\n{reset_link}"
            send_mail(subject, message, 'abhooman344@gmail.com', [user.email])

            messages.success(request, "Password reset link has been sent to your email.")
        else:
            messages.error(request, "Email address not found.")
    
    return render(request, 'users/request_password_reset.html')

def reset_password(request, token):
    reset_token = get_object_or_404(PasswordResetToken, token=token)

    if not reset_token.is_valid():
        messages.error(request, "This reset link has expired.")
        return render(request, 'users/reset_password_expired.html')

    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('password_confirm')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'users/reset_password.html', {'token': token})

        user = reset_token.user
        user.password = make_password(new_password)
        user.save()

        reset_token.delete()

        messages.success(request, "Your password has been reset successfully.")
        return redirect('login')

    return render(request, 'users/reset_password.html', {'token': token})
