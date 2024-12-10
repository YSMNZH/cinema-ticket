import os
import django
from datetime import datetime

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_ticket.settings')
django.setup()

from main.models import Movie

# Data for movies
movies_data = [
    {
        "title": "Interstellar",
        "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "release_date": "2014-11-07",
        "duration_minutes": 169,
        "genre": "Science Fiction",
        "poster": "posters/interstellar",
        "imdb_rating": 8.6,
    },
    {
        "title": "Inception",
        "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.",
        "release_date": "2010-07-16",
        "duration_minutes": 148,
        "genre": "Action, Adventure, Sci-Fi",
        "poster": "posters/inception",
        "imdb_rating": 8.8,
    },
    {
        "title": "The Dark Knight",
        "description": "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.",
        "release_date": "2008-07-18",
        "duration_minutes": 152,
        "genre": "Action, Crime, Drama",
        "poster": "posters/thedarkknight",
        "imdb_rating": 9.0,
    },
    {
        "title": "Parasite",
        "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        "release_date": "2019-05-30",
        "duration_minutes": 132,
        "genre": "Drama, Thriller",
        "poster": "posters/parasite",
        "imdb_rating": 8.6,
    },
    {
        "title": "The Shawshank Redemption",
        "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "release_date": "1994-09-23",
        "duration_minutes": 142,
        "genre": "Drama",
        "poster": "posters/shawshank",
        "imdb_rating": 9.3,
    }
]

# Adding movies to the database
try:
    for movie_data in movies_data:
        movie, created = Movie.objects.get_or_create(
            title=movie_data["title"],
            defaults={
                "description": movie_data["description"],
                "release_date": datetime.strptime(movie_data["release_date"], "%Y-%m-%d"),
                "duration_minutes": movie_data["duration_minutes"],
                "genre": movie_data["genre"],
                "poster": movie_data["poster"],
                "imdb_rating": movie_data["imdb_rating"],
            }
        )
        if created:
            print(f"Added movie: {movie.title}")
        else:
            print(f"Movie already exists: {movie.title}")
except Exception as e:
    print(f"An error occurred: {e}")
