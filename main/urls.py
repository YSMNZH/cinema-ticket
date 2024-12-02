from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main, name='main'),
    path('contact/', views.contact, name='contact'),
    path('news/', views.news, name='news'),
    path('movie/', views.movie, name='movie'),
    path('', views.index, name='index'),
]
