from django.urls import path
<<<<<<< HEAD
from .views import MovieListView, BookTicketView
from .views import RegisterView
from .views import LoginView
from .views import UserPanelView
from . import views

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('tickets/book/', BookTicketView.as_view(), name='book_ticket'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('panel/', UserPanelView.as_view(), name='user_panel'),
    path('request-password-reset/', views.request_password_reset, name='request_password_reset'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    
=======
from .views import  MovieListView, BookTicketView
from . import views
urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('tickets/book/', BookTicketView.as_view(), name='book_ticket'),
>>>>>>> 050a0c8c64b710a433556971b1fb227f5ee59588
]
