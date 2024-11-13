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
