from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages
from .models import Movie
from django.shortcuts import render
from .models import Movie
from main.ticket_generator import generate_ticket_pdf
import os
from django.http import FileResponse,HttpResponse
from django.shortcuts import get_object_or_404
from .models import Ticket,News
from django.db.models import Q
from django.http import JsonResponse

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


