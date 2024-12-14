from django.urls import path
from . import views
# from .views import search_movies

urlpatterns = [
    path('main/', views.main, name='main'),
    path('contact/', views.contact, name='contact'),
    path('news/', views.news, name='news'),
    path('movie/', views.movie, name='movie'),
    path('', views.index, name='index'),
    # path('search/', search_movies, name='search_movies'),
]
