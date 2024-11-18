from django.contrib import admin
from django.urls import path, include
from WolMain import views as wolmain_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('WolApi.urls')),
    path('', wolmain_views.home, name='home'), 
]
