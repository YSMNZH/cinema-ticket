from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def main(request):
    return render(request, "main/main.html")

def contact(request):
    return render(request, "main/contact.html")