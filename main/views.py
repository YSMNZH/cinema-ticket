from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages
from .models import Movie,ShowTime,Seat,Cinema,Hall
from django.shortcuts import render
from main.ticket_generator import generate_ticket_pdf
import os
from django.http import FileResponse,HttpResponse
from django.shortcuts import get_object_or_404
from .models import Ticket,News,ShowTime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.db import IntegrityError
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponseNotAllowed

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('../../main/main')
    else:
        return HttpResponseNotAllowed(['POST'])
    
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


# def search_movies(request):
#     query = request.GET.get('q', '')
#     if query:
#         movies = Movie.objects.filter(
#             Q(title__icontains=query) | Q(description__icontains=query)
#         )
#     else:
#         movies = Movie.objects.none()
    
#     movies_data = list(movies.values('id', 'title', 'genre', 'duration_minutes', 'release_date', 'imdb_rating', 'poster'))
#     return JsonResponse({'movies': movies_data})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact') 
        else:
            messages.error(request, 'There was an error in your form. Please try again.')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})

def news(request):
    my_news = News.objects.all()
    return render(request, "main/news.html", {"news": my_news})

def movie(request):
    return render(request, "main/movie.html")

def index(request):
    return render(request, 'index.html')

from django.db import transaction
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
import os

def download_ticket(request, ticket_id):
    ticket = get_object_or_404(
        Ticket.objects.select_related('seat__hall__cinema', 'show_time__movie'), id=ticket_id
    )

    try:
        # Atomic block to ensure only one user can reserve the ticket
        with transaction.atomic():
            # Reload ticket within the transaction to get the latest data
            ticket = Ticket.objects.select_for_update().get(id=ticket_id)

            if not ticket.is_reserved:
                return HttpResponse("This ticket has not been reserved yet.", status=400)

            if ticket.is_locked:  # Add an "is_locked" field to Ticket to indicate it's being processed
                return HttpResponse("This ticket is being processed by another user.", status=409)

            # Lock the ticket for processing
            ticket.is_locked = True
            ticket.save()

        # Generate ticket data
        ticket_data = {
            "Name": ticket.customer_name,
            "Movie": ticket.show_time.movie.title,
            "Cinema": ticket.seat.hall.cinema.name,
            "City": ticket.seat.hall.cinema.city.name,
            "Hall": ticket.seat.hall.hall_number,
            "Seat": f"Row {ticket.seat.row_number}, Seat {ticket.seat.seat_number}",
            "Show Time": ticket.show_time.start_time.strftime("%Y-%m-%d %H:%M"),
            "Price": f"{ticket.price} IRR"
        }

        # Generate PDF
        output_path = f"ticket_{ticket.id}.pdf"
        generate_ticket_pdf(ticket_data, output_path=output_path)

        # Unlock the ticket after successful processing
        with transaction.atomic():
            ticket.is_locked = False
            ticket.save()

        # Serve the PDF
        response = FileResponse(open(output_path, "rb"), content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.id}.pdf"'

        # Optionally clean up the file after serving
        os.remove(output_path)

        return response

    except Exception as e:
        # Handle errors
        if ticket:
            with transaction.atomic():
                ticket.is_locked = False
                ticket.save()
        return HttpResponse(f"An error occurred: {e}", status=500)

def news_page(request):
    news_list = News.objects.all().order_by('-create_at') 
    return render(request, 'news.html', {'news_list': news_list})

from django.shortcuts import render, get_object_or_404
from .models import Movie, Cinema, ShowTime, Seat
from django.views.decorators.cache import never_cache

@never_cache
@login_required
def reservation(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    step = request.GET.get('step', 'cinema')
    cinemas = showtimes = rows = reserved_seats = None
    selected_cinema_id = request.GET.get('cinema_id')
    selected_showtime_id = request.GET.get('showtime_id')

    if step == 'cinema':
        cinemas = Cinema.objects.all()

    elif step == 'showtime' and selected_cinema_id:
        showtimes = ShowTime.objects.filter(movie=movie, hall__cinema_id=selected_cinema_id)

    elif step == 'seats' and selected_showtime_id:
        selected_showtime = get_object_or_404(ShowTime, id=selected_showtime_id)
        seats = Seat.objects.filter(hall=selected_showtime.hall)
        
        rows = [
            seats.filter(row_number=row).order_by('seat_number') 
            for row in range(1, 11)
        ]

        reserved_seats = Ticket.objects.filter(show_time=selected_showtime, is_reserved=True).values_list('seat_id', flat=True)

        if request.method == 'POST':
            data = json.loads(request.body)
            selected_seat_ids = data.get('seats', [])
            if not selected_seat_ids:
                return JsonResponse({'success': False, 'error': 'No seats selected.'})

            for seat_id in selected_seat_ids:
                ticket = Ticket.objects.filter(seat_id=seat_id, show_time=selected_showtime, is_reserved=True).first()
                if ticket:
                    return JsonResponse({'success': False, 'error': f"Seat {ticket.seat.row_number}-{ticket.seat.seat_number} is already reserved."})
                
                try:
                    Ticket.objects.create(
                        customer_name=request.user.username,
                        seat_id=seat_id,
                        show_time=selected_showtime,
                        price=50000,
                        is_reserved=True,
                    )
                except IntegrityError:
                    return JsonResponse({'success': False, 'error': "This seat is already reserved."})

            return JsonResponse({'success': True, 'show_time_id': selected_showtime_id})

    context = {
        'movie': movie,
        'step': step,
        'cinemas': cinemas,
        'showtimes': showtimes,
        'rows': rows,
        'reserved_seats': reserved_seats,
        'user_logged_in': request.user.is_authenticated,
    }
    return render(request, 'main/reservation.html', context)


@login_required
def reservation_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'main/reservation.html', {'movie': movie})

@login_required
def reservation_cinema(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    cinemas = Cinema.objects.all()
    return render(request, 'main/reservation.html', {'movie': movie, 'cinemas': cinemas, 'step': 2})

@login_required
def reservation_showtime(request, movie_id, cinema_id):
    showtimes = ShowTime.objects.filter(movie_id=movie_id, hall__cinema_id=cinema_id)
    return render(request, 'main/reservation.html', {'showtimes': showtimes, 'step': 3})

@login_required
def reservation_seats(request, movie_id, cinema_id, showtime_id):
    seats = Seat.objects.filter(hall__showtime__id=showtime_id)
    return render(request, 'main/reservation.html', {'seats': seats, 'step': 4})

@login_required
def confirmation(request):
    show_time_id = request.GET.get('show_time_id')
    selected_show_time = get_object_or_404(ShowTime, id=show_time_id)
    tickets = Ticket.objects.filter(customer_name=request.user.username, show_time=selected_show_time, is_reserved=True)

    if tickets.exists():
        seats = [f"Row {ticket.seat.row_number}, Seat {ticket.seat.seat_number}" for ticket in tickets]
        reservation_details = {
            "name": request.user.name or "N/A",
            "family_name": request.user.family_name or "N/A",
            "num_tickets": tickets.count(),
            "seats": seats,
            "cinema": selected_show_time.hall.cinema.name,
            "movie": selected_show_time.movie.title,
        }
    else:
        reservation_details = {
            "name": "N/A",
            "family_name": "N/A",
            "num_tickets": 0,
            "seats": [],
            "cinema": "N/A",
            "movie": "N/A",
        }

    return render(request, 'main/confirmation.html', {'reservation_details': reservation_details})



# def search_view(request):
#     query = request.GET.get('q', '')
#     if query:
#         results = Movie.objects.filter(
#             title__icontains=query
#         ) | Movie.objects.filter(
#             description__icontains=query 
#         )
#     else:
#         results = Movie.objects.none()
#     return render(request,  'main/search_results.html', {'results': results, 'query': query})
