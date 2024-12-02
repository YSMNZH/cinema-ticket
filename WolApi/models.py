from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from datetime import timedelta

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Cinema(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="halls")
    name = models.CharField(max_length=100)
    seat_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.cinema.name}"


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    showtime = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} at {self.showtime} in {self.hall.name}"


class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="seats")
    row = models.CharField(max_length=1)  # برای مثال A, B, C
    number = models.PositiveIntegerField()

    def __str__(self):
        return f"Seat {self.row}{self.number} in {self.hall.name}"


class Ticket(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_time = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Ticket for {self.showtime.movie.title} on {self.showtime.showtime} - Seat {self.seat}"
    
class Users(models.Model):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

def get_expiration_time():
    return now() + timedelta(hours=1)

class PasswordResetTokens(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField(default=get_expiration_time)
    created_at = models.DateTimeField(default=now)
