import os
import django
from django.db import transaction, IntegrityError
from datetime import datetime, timedelta, time
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_ticket.settings')
django.setup()

from main.models import City, Cinema, Hall, Seat, Ticket, ShowTime, Movie

try:
    with transaction.atomic():
        Ticket.objects.all().delete()
        ShowTime.objects.all().delete()
        Seat.objects.all().delete()
        Hall.objects.all().delete()
        Cinema.objects.all().delete()
        City.objects.all().delete()
        print("All existing data has been deleted.")

        # Step 1: Adding cities
        cities_data = ["Tehran", "Mashhad", "Isfahan", "Shiraz", "Tabriz"]
        cities = City.objects.bulk_create(
            [City(name=city_name) for city_name in cities_data],
            ignore_conflicts=True
        )
        print(1)

        # Step 2: Adding cinemas to each city
        cinemas_data = {
            "Tehran": ["Azadi Cinema", "Mellat Cinema", "Iran Cinema"],
            "Mashhad": ["Hoveizeh Cinema", "Simorgh Cinema"],
            "Isfahan": ["Sahel Cinema", "Sepahan Cinema"],
            "Shiraz": ["Saadi Cinema", "City of Sun Cinema"],
            "Tabriz": ["22 Bahman Cinema", "Naji Cinema"]
        }
        print(2)

        cinemas = []
        for city_name, cinema_names in cinemas_data.items():
            city = City.objects.get(name=city_name)
            for cinema_name in cinema_names:
                cinemas.append(Cinema(name=cinema_name, city=city))
        Cinema.objects.bulk_create(cinemas, ignore_conflicts=True)
        print(3)

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
        print(4)

        seats = []
        all_halls = Hall.objects.all()
        for hall in all_halls:
            for row in range(1, 11):
                for seat_number in range(1, 16):
                    Seat.objects.get_or_create(hall_id=hall.id, row_number=row, seat_number=seat_number)

        print("Seats created.")

        # Step 4: Adding random showtimes for movies
        movies = Movie.objects.all()

        start_times = [time(hour, 0) for hour in range(14, 23)]  # Possible start times
        showtimes = []

        for hall in all_halls:
            random_movies = random.sample(list(movies), min(len(movies), 5))  # Select random movies for each hall

            assigned_times = set()  # Track assigned times to avoid duplicates
            for movie in random_movies:
                while True:
                    random_time = random.choice(start_times)
                    if random_time not in assigned_times:
                        assigned_times.add(random_time)
                        show_date = datetime.combine(datetime.now().date() + timedelta(days=1), random_time)
                        showtimes.append(ShowTime(movie=movie, hall=hall, start_time=show_date))
                        break
        ShowTime.objects.bulk_create(showtimes, ignore_conflicts=True)

        print("Showtimes created.")

        # Step 5: Adding sample tickets
        tickets = []
        sample_seats = Seat.objects.all()[:50] 
        sample_showtime = ShowTime.objects.first()
        for seat in sample_seats:
            tickets.append(
                Ticket(
                    seat=seat,
                    show_time=sample_showtime,
                    price=50000,
                    is_reserved=False
                )
            )
        Ticket.objects.bulk_create(tickets, ignore_conflicts=True)

        print("All data successfully reset and added!")

except IntegrityError as e:
    print(f"An error occurred: {e}")