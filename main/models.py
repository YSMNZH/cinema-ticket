from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration_minutes = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='posters/')
    imdb_rating = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Cinema(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="cinemas")

    def __str__(self):
        return f"{self.name} - {self.city.name}"


class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="halls")
    hall_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ("cinema", "hall_number")

    def __str__(self):
        return f"Hall {self.hall_number} - {self.cinema.name}"


class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="seats")
    row_number = models.PositiveIntegerField()
    seat_number = models.CharField(max_length=10)

    # class Meta:
    #     unique_together = ("hall", "seat_number")

    def __str__(self):
        return f"Seat {self.seat_number} in Row {self.row_number}, {self.hall}"


class ShowTime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="showtimes")
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="showtimes")
    start_time = models.DateTimeField()

    class Meta:
        unique_together = ("movie", "hall", "start_time")

    def __str__(self):
        return f"{self.movie.title} at {self.start_time} in {self.hall}"


class Ticket(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="tickets")
    show_time = models.ForeignKey(ShowTime, on_delete=models.CASCADE, related_name="tickets")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_reserved = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    customer_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ("seat", "show_time")

    def __str__(self):
        return f"Ticket for {self.seat} - {self.show_time}"
    
class News(models.Model):
    title = models.CharField(max_length= 255)
    text = models.TextField()
    image_url = models.URLField(max_length=500,blank=True,null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
