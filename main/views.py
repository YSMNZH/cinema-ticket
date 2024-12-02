from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages
from .models import Movie

from django.shortcuts import render
from .models import Movie

def main(request):
    movies = Movie.objects.all()
    if request.method == "POST":
        genre = request.POST.get('genre', '')
        year = request.POST.get('year', '')
        score = request.POST.get('score', '')
        print(genre)

        if genre:
            movies = movies.filter(genre__icontains=genre)
        if year:
            movies = movies.filter(release_date__year=year)
        if score:
            score_range = score.split('-')
            if len(score_range) == 2:
                min_score, max_score = map(float, score_range)
                movies = movies.filter(imdb_rating__gte=min_score, imdb_rating__lte=max_score)

    return render(request, 'main/main.html', {'movies': movies})

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
