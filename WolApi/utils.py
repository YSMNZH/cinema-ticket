import random
import string
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from .models import Ticket

OTP_EXPIRY_TIME = 300  # 5 دقیقه

def generate_otp(identifier, length=6):
    digits = string.digits
    otp = ''.join(random.choices(digits, k=length))
    cache.set(identifier, otp, timeout=OTP_EXPIRY_TIME)
    return otp

def validate_otp(identifier, otp):
    cached_otp = cache.get(identifier)
    if cached_otp is not None and cached_otp == otp:
        cache.delete(identifier)
        return True
    return False

def calculate_ticket_price(base_price, discount=0, tax_rate=0.1):
    discounted_price = base_price * (1 - discount)
    final_price = discounted_price * (1 + tax_rate)
    return round(final_price, 2)

def format_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def is_seat_available(showtime, seat):
    return not Ticket.objects.filter(showtime=showtime, seat=seat).exists()

def send_ticket_confirmation(user_email, ticket_details):
    subject = 'تأیید خرید بلیط سینما'
    message = f"جزئیات بلیط شما:\n{ticket_details}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)
