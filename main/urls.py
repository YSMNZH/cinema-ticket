from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth.views import LogoutView
# from .views import search_movies

urlpatterns = [
    path('main/', views.main, name='main'),
    path('contact/', views.contact, name='contact'),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path('news/', views.news, name='news'),
    path('movie/', views.movie, name='movie'),
    path('', views.index, name='index'),
    path('reservation/<int:movie_id>/', views.reservation, name='reservation'),
    path('reservation/<int:movie_id>/', views.reservation_movie, name='reservation_movie'),
    path('reservation/<int:movie_id>/cinema/', views.reservation_cinema, name='reservation_cinema'),
    path('reservation/<int:movie_id>/cinema/<int:cinema_id>/', views.reservation_showtime, name='reservation_showtime'),
    path('reservation/<int:movie_id>/cinema/<int:cinema_id>/showtime/<int:showtime_id>/', views.reservation_seats, name='reservation_seats'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('download-ticket/', views.generate_ticket_pdf, name='download_ticket'),
]
