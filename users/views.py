from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate
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
from django.contrib.auth.decorators import login_required
from main.models import Movie
    
def main(request):
    movies = Movie.objects.all()

    query = request.GET.get('q', '') 
    if query:
        movies = Movie.objects.filter(
            title__icontains=query
        ) | Movie.objects.filter(
            description__icontains=query 
        )

    if request.method == "POST":
        genre = request.POST.get('genre', '')
        year = request.POST.get('year', '')
        score = request.POST.get('score', '')

        if genre:
            movies = movies.filter(genre__icontains=genre)
        if year:
            movies = movies.filter(release_date__year=year)
        if score:
            score_range = score.split('-')
            if len(score_range) == 2:
                min_score, max_score = map(float, score_range)
                movies = movies.filter(imdb_rating__gte=min_score, imdb_rating__lte=max_score)

    return render(request, 'main/main.html', {'movies': movies, 'query': query})

from django.views.decorators.cache import never_cache

@never_cache
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            request.session['user_name'] = user.name
            request.session['user_email'] = user.email
            return redirect('../../main/main') 
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

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.name = request.POST.get('name', user.name)
        user.family_name = request.POST.get('family_name', user.family_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.date_birth = request.POST.get('date_birth', user.date_birth)

        password = request.POST.get('password', None)
        if password:
            user.set_password(password)

        try:
            user.save()
            messages.success(request, 'Your profile has been updated successfully!')
        except Exception as e:
            messages.error(request, f"Error updating profile: {e}")

        return redirect('profile')  

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
