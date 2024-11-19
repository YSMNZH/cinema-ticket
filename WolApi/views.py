from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Cinema, Hall, Showtime, Seat, Ticket
from django.contrib.auth.models import User
from .serializers import MovieSerializer, CinemaSerializer, HallSerializer, ShowtimeSerializer, SeatSerializer, TicketSerializer
from .serializers import RegisterSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate
import secrets
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from .models import Users, PasswordResetTokens


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
        
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                "message": "Login successful",
                "username": user.username,
                "token": token.key
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserPanelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_data = {
            "username": request.user.username,
            "email": request.user.email,
        }
        return Response(user_data)
    
def request_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = Users.objects.filter(email=email).first()
        if user:
            token = get_random_string(64)
            expires_at = now() + timedelta(hours=1)
            
            PasswordResetTokens.objects.create(user_id=user.id, token=token, expires_at=expires_at)
            
            reset_link = f"http://localhost:8000/reset-password/{token}"  # لینک بازنشانی رمز عبور
            send_mail(
                'Password Reset Request',
                f'Use the following link to reset your password: {reset_link}',
                'no-reply@yourdomain.com', 
                [email],
            )
            return JsonResponse({'status': 'success', 'message': 'Password reset email sent.'})
        return JsonResponse({'status': 'error', 'message': 'Email not found.'})
    
def reset_password(request, token):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        reset_token = get_object_or_404(PasswordResetTokens, token=token)
        
        if reset_token.expires_at < now():
            return JsonResponse({'status': 'error', 'message': 'Token has expired.'})
        
        user = reset_token.user
        user.password_hash = new_password 
        user.save()
        
        reset_token.delete()
        
        return JsonResponse({'status': 'success', 'message': 'Password updated successfully.'})
        
    return render(request, 'reset_password_form.html', {'token': token})
