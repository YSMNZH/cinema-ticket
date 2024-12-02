from django.db import models

# Roles Table
class Role(models.Model):
    RoleName = models.CharField(max_length=15)
    Description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Roles'

    def __str__(self):
        return self.RoleName


# Permissions Table
class Permission(models.Model):
    Action = models.CharField(max_length=50)

    class Meta:
        db_table = 'Permissions'

    def __str__(self):
        return self.Action


# RolePermissions Table (Many-to-Many relationship using Django's ManyToManyField)
Role.permissions = models.ManyToManyField(Permission, through='RolePermission', related_name='roles')


# RolePermission as a through table for the ManyToMany relationship
class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        db_table = 'RolePermissions'
        unique_together = ('role', 'permission')


# Users Table
class User(models.Model):
    RoleID = models.ForeignKey(Role, on_delete=models.CASCADE)
    Name = models.CharField(max_length=20)
    FamilyName = models.CharField(max_length=20)
    BirthDate = models.DateField()
    PhoneNumber = models.CharField(max_length=15, unique=True)
    Email = models.EmailField(max_length=255, unique=True)
    Password = models.TextField()

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return f"{self.Name} {self.FamilyName}"


# Provinces Table
class Province(models.Model):
    ProvinceName = models.CharField(max_length=50)

    class Meta:
        db_table = 'Provinces'

    def __str__(self):
        return self.ProvinceName


# Cities Table
class City(models.Model):
    CityName = models.CharField(max_length=50)
    ProvinceID = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Cities'

    def __str__(self):
        return self.CityName


# Cinemas Table
class Cinema(models.Model):
    CinemaName = models.CharField(max_length=100)
    CityID = models.ForeignKey(City, on_delete=models.CASCADE)
    ProvinceID = models.ForeignKey(Province, on_delete=models.CASCADE)
    Address = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Cinemas'

    def __str__(self):
        return self.CinemaName


# Movies Table
class Movie(models.Model):
    Title = models.CharField(max_length=255)
    Genre = models.CharField(max_length=50)
    DurationMinutes = models.IntegerField()
    ReleaseDate = models.DateField()
    Rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)

    class Meta:
        db_table = 'Movies'

    def __str__(self):
        return self.Title


# Screenings Table
class Screening(models.Model):
    AuditoriumID = models.IntegerField(unique=True)
    MovieID = models.ForeignKey(Movie, on_delete=models.CASCADE)
    CinemaID = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    StartTime = models.DateTimeField()
    EndTime = models.DateTimeField()
    Capacity = models.IntegerField()

    class Meta:
        db_table = 'Screenings'


# Seats Table
class Seat(models.Model):
    AuditoriumID = models.ForeignKey(Screening, on_delete=models.CASCADE, to_field='AuditoriumID')

    class Meta:
        db_table = 'Seats'


# Tickets Table
class Ticket(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    SeatID = models.ForeignKey(Seat, on_delete=models.CASCADE)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    PurchaseDateTime = models.DateTimeField()

    class Meta:
        db_table = 'Tickets'


# Reviews Table
class Review(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    MovieID = models.ForeignKey(Movie, on_delete=models.CASCADE)
    Rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    ReviewText = models.TextField(null=True, blank=True)
    ReviewDate = models.DateTimeField()

    class Meta:
        db_table = 'Reviews'

class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="halls")
    name = models.CharField(max_length=100)
    seat_count = models.PositiveIntegerField()
class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    showtime = models.DateTimeField()from django.db import models
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
