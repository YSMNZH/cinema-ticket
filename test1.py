import os
import django
from django.db import transaction, IntegrityError
from datetime import datetime, timedelta

# تنظیم متغیر محیطی برای استفاده از تنظیمات جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_ticket.settings')  # نام پروژه را بررسی کنید
django.setup()

from main.models import City, Cinema, Hall, Seat, Ticket, ShowTime, Movie

try:
    with transaction.atomic():
        # Step 1: Adding cities
        cities_data = ["Tehran", "Mashhad", "Isfahan", "Shiraz", "Tabriz"]
        cities = City.objects.bulk_create(
            [City(name=city_name) for city_name in cities_data],
            ignore_conflicts=True
        )

        # Step 2: Adding cinemas to each city
        cinemas_data = {
            "Tehran": ["Azadi Cinema", "Mellat Cinema", "Iran Cinema"],
            "Mashhad": ["Hoveizeh Cinema", "Simorgh Cinema"],
            "Isfahan": ["Sahel Cinema", "Sepahan Cinema"],
            "Shiraz": ["Saadi Cinema", "City of Sun Cinema"],
            "Tabriz": ["22 Bahman Cinema", "Naji Cinema"]
        }

        cinemas = []
        for city_name, cinema_names in cinemas_data.items():
            city = City.objects.get(name=city_name)
            for cinema_name in cinema_names:
                cinemas.append(Cinema(name=cinema_name, city=city))
        Cinema.objects.bulk_create(cinemas, ignore_conflicts=True)

        # Step 3: Adding halls to each cinema
        halls_data = {
            "Azadi Cinema": 3,
            "Mellat Cinema": 4,
            "Iran Cinema": 2,
            "Hoveizeh Cinema": 5,
            "Simorgh Cinema": 3,
            "Sahel Cinema": 2,
            "Sepahan Cinema": 3,
            "Saadi Cinema": 2,
            "City of Sun Cinema": 4,
            "22 Bahman Cinema": 3,
            "Naji Cinema": 2
        }

        halls = []
        for cinema_name, hall_count in halls_data.items():
            cinema = Cinema.objects.get(name=cinema_name)
            for i in range(1, hall_count + 1):
                halls.append(Hall(cinema=cinema, hall_number=i))
        Hall.objects.bulk_create(halls, ignore_conflicts=True)

        # Step 4: Adding seats to each hall
        seats = []
        all_halls = Hall.objects.all()
        for hall in all_halls:
            for row in range(1, 11):  # Assuming 10 rows
                for number in range(1, 21):  # Assuming 20 seats per row
                    seats.append(Seat(hall=hall, row_number=row, seat_number=number))
        Seat.objects.bulk_create(seats, ignore_conflicts=True)

        # Step 5: Adding movies
        movies = [
            Movie(title="Inception", description="A mind-bending thriller", release_date=datetime(2010, 7, 16),
                  duration_minutes=148, genre="Sci-Fi", imdb_rating=8.8),
            Movie(title="The Dark Knight", description="Batman vs Joker", release_date=datetime(2008, 7, 18),
                  duration_minutes=152, genre="Action", imdb_rating=9.0)
        ]
        Movie.objects.bulk_create(movies, ignore_conflicts=True)
        all_movies = Movie.objects.all()

        # Step 6: Adding showtimes
        showtimes = []
        for hall in all_halls:
            for movie in all_movies[:2]:  # Assign first 2 movies to all halls
                start_time = datetime.now() + timedelta(days=1)  # Show time for tomorrow
                showtimes.append(ShowTime(movie=movie, hall=hall, start_time=start_time))
        ShowTime.objects.bulk_create(showtimes, ignore_conflicts=True)

        # Step 7: Adding sample tickets
        tickets = []
        sample_seats = Seat.objects.all()[:50]  # Creating tickets for the first 50 seats as an example
        sample_showtime = ShowTime.objects.first()  # Assign the first showtime to all tickets
        for seat in sample_seats:
            tickets.append(
                Ticket(
                    seat=seat,
                    show_time=sample_showtime,  # Must be a ShowTime instance
                    price=50000,
                    is_reserved=False
                )
            )
        Ticket.objects.bulk_create(tickets, ignore_conflicts=True)

        print("Data successfully added!")

except IntegrityError as e:
    print(f"An error occurred: {e}")
