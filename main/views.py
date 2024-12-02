from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages

def main(request):
    return render(request, "main/main.html")

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