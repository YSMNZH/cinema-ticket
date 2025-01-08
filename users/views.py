from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
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
from main.models import ShowTime,Ticket
import pytz
from django.views.decorators.cache import never_cache


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

iran_tz = pytz.timezone('Asia/Tehran')

@login_required
def profile(request):
    reservation_details = []

    show_time_id = request.GET.get('show_time_id')

    if show_time_id:
        selected_show_time = get_object_or_404(ShowTime, id=show_time_id)
        
        tickets = Ticket.objects.filter(
            customer_name=request.user.username,
            show_time=selected_show_time,
            is_reserved=True
        )

        if tickets.exists():
            seats = [f"Row {ticket.seat.row_number}, Seat {ticket.seat.seat_number}" for ticket in tickets]

            show_time_iran = selected_show_time.start_time.astimezone(iran_tz)
            formatted_show_time = show_time_iran.strftime('%Y-%m-%d %H:%M:%S')

            reservation_iran = tickets.first().reservation_date.astimezone(iran_tz)
            formatted_reservation_date = reservation_iran.strftime('%Y-%m-%d %H:%M:%S')

            reservation_details.append({
                "name": request.user.name or "N/A",
                "family_name": request.user.family_name or "N/A",
                "num_tickets": tickets.count(),
                "seats": seats,
                "cinema": selected_show_time.hall.cinema.name,
                "movie": selected_show_time.movie.title,
                "movie_time": formatted_show_time,  
                "reservation_date": formatted_reservation_date,  
            })
    else:
        tickets = Ticket.objects.filter(
            customer_name=request.user.username,
            is_reserved=True
        )

        showtimes_seen = set()

        for ticket in tickets:
            show_time = ticket.show_time
            if show_time.id not in showtimes_seen:
                showtimes_seen.add(show_time.id)

                seats = [f"Row {ticket.seat.row_number}, Seat {ticket.seat.seat_number}" for ticket in tickets if ticket.show_time == show_time]

                show_time_iran = show_time.start_time.astimezone(iran_tz)
                formatted_show_time = show_time_iran.strftime('%Y-%m-%d %H:%M:%S')

                reservation_iran = ticket.reservation_date.astimezone(iran_tz)
                formatted_reservation_date = reservation_iran.strftime('%Y-%m-%d %H:%M:%S')

                reservation_details.append({
                    "name": request.user.name or "N/A",
                    "family_name": request.user.family_name or "N/A",
                    "num_tickets": tickets.filter(show_time=show_time).count(),
                    "seats": seats,
                    "cinema": show_time.hall.cinema.name,
                    "movie": show_time.movie.title,
                    "movie_time": formatted_show_time,
                    "reservation_date": formatted_reservation_date,
                })

    return render(request, 'users/profile.html', {
        'reservation_details': reservation_details,
        'show_time_id': show_time_id,
        'user': request.user
    })

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
