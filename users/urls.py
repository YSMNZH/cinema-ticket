# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'), 
    path('register/', views.register_view, name='register'),
    path('', views.main_view, name='main'),
    path('edit/', views.edit_view, name='edit'),
]
