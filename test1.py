import os
import django
from django.db import transaction, IntegrityError
from datetime import datetime, timedelta

# تنظیم متغیر محیطی برای استفاده از تنظیمات جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_ticket.settings')  # نام پروژه را بررسی کنید و جایگزین کنید
django.setup()

from main.models import City, Cinema, Hall, Seat, Ticket

try:
    with transaction.atomic():
        # Step 1: Adding cities
        cities_data = ["Tehran", "Mashhad", "Isfahan", "Shiraz", "Tabriz"]
        cities = []
        for city_name in cities_data:
            city, created = City.objects.get_or_create(name=city_name)
            cities.append(city)

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
                cinema, created = Cinema.objects.get_or_create(name=cinema_name, city=city)
                cinemas.append(cinema)

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
                hall, created = Hall.objects.get_or_create(cinema=cinema, hall_number=i)
                halls.append(hall)

        # Step 4: Adding seats to each hall
        seats = []
        for hall in halls:
            for row in range(1, 11):  # Assuming 10 rows
                for number in range(1, 21):  # Assuming 20 seats per row
                    seat, created = Seat.objects.get_or_create(hall=hall, row=row, seat_number=number)
                    seats.append(seat)

        # Step 5: Adding sample tickets
        tickets = []
        for seat in seats[:50]:  # Creating tickets for the first 50 seats as an example
            ticket, created = Ticket.objects.get_or_create(
                seat=seat,
                price=50000,
                show_time=datetime.now() + timedelta(days=1),  # Show time for tomorrow
                customer_name=f"Customer {seat.id}"
            )
            tickets.append(ticket)

        print("Data successfully added!")

except IntegrityError as e:
    print(f"An error occurred: {e}")
