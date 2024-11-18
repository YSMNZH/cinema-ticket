from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Cinema, Hall, Showtime, Seat, Ticket
from django.contrib.auth.models import User
from .serializers import MovieSerializer, CinemaSerializer, HallSerializer, ShowtimeSerializer, SeatSerializer, TicketSerializer

class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


class BookTicketView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        showtime_id = request.data.get('showtime_id')
        seat_id = request.data.get('seat_id')

        try:
            user = User.objects.get(id=user_id)
            showtime = Showtime.objects.get(id=showtime_id)
            seat = Seat.objects.get(id=seat_id)

            if Ticket.objects.filter(showtime=showtime, seat=seat).exists():
                return Response({"error": "This seat is already booked."}, status=status.HTTP_400_BAD_REQUEST)

            ticket = Ticket.objects.create(showtime=showtime, seat=seat, user=user, price=100)

            return Response({"message": "Ticket booked successfully", "ticket_id": ticket.id}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Showtime.DoesNotExist:
            return Response({"error": "Showtime not found"}, status=status.HTTP_404_NOT_FOUND)
        except Seat.DoesNotExist:
            return Response({"error": "Seat not found"}, status=status.HTTP_404_NOT_FOUND)
        

