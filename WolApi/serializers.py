from rest_framework import serializers
from .models import Movie, Cinema, Hall, Showtime, Seat, Ticket

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = '__all__'


class HallSerializer(serializers.ModelSerializer):
    cinema = CinemaSerializer()

    class Meta:
        model = Hall
        fields = '__all__'


class ShowtimeSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    hall = HallSerializer()

    class Meta:
        model = Showtime
        fields = '__all__'


class SeatSerializer(serializers.ModelSerializer):
    hall = HallSerializer()

    class Meta:
        model = Seat
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    showtime = ShowtimeSerializer()
    seat = SeatSerializer()

    class Meta:
        model = Ticket
        fields = '__all__'
