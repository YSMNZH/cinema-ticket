from django.urls import path
from .views import MovieListView, BookTicketView
from .views import RegisterView
from .views import LoginView
from .views import UserPanelView

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('tickets/book/', BookTicketView.as_view(), name='book_ticket'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('panel/', UserPanelView.as_view(), name='user_panel'),
]
