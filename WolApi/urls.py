from django.urls import path
from .views import  MovieListView, BookTicketView
from . import views
urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('tickets/book/', BookTicketView.as_view(), name='book_ticket'),
]
