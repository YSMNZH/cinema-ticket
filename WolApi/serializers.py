from rest_framework import serializers
from .models import Movie, Cinema, Hall, Showtime, Seat, Ticket
<<<<<<< HEAD
from django.contrib.auth.models import User
=======
>>>>>>> 050a0c8c64b710a433556971b1fb227f5ee59588

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
<<<<<<< HEAD

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
=======
>>>>>>> 050a0c8c64b710a433556971b1fb227f5ee59588
