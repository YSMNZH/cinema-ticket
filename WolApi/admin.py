from django.contrib import admin
from .models import Movie, Cinema, Hall, Seat, Showtime, Ticket

admin.site.register(Movie)
admin.site.register(Cinema)
admin.site.register(Hall)
admin.site.register(Seat)
admin.site.register(Showtime)
admin.site.register(Ticket)
