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
from .models import Ticket

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
    return render(request, "main/news.html")

def movie(request):
    return render(request, "main/movie.html")

def index(request):
    return render(request, 'index.html')

def download_ticket(request, ticket_id):
    # دریافت بلیت
    ticket = get_object_or_404(Ticket.objects.select_related('seat__hall__cinema', 'show_time__movie'), id=ticket_id)

    try:
        if not ticket.is_reserved:
            return HttpResponse("This ticket has not been reserved yet.", status=400)

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

        output_path = f"ticket_{ticket.id}.pdf"

        generate_ticket_pdf(ticket_data, output_path=output_path)

        response = FileResponse(open(output_path, "rb"), content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.id}.pdf"'

        return response

    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
    
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


