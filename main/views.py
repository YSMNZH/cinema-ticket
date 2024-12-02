from django.shortcuts import render

def main(request):
    return render(request, "main/main.html")

def contact(request):
    return render(request, "main/contact.html")

def news(request):
    return render(request, "main/news.html")

def movie(request):
    return render(request, "main/movie.html")