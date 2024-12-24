
from django.urls import path
from . import views
from main.views import main

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.update_profile, name='update_profile'),
    path('forgot-password/', views.request_password_reset, name='forgot-password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('main/main', views.main, name='main'),
]
