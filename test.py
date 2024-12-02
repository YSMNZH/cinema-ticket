from django.core.mail import send_mail
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_ticket.settings')

import django
django.setup()

subject = 'Welcome to My Website'
message = 'Thank you for registering on our website.'
from_email = 'abhooman344@gmail.com'
recipient_list = ['abhooman7@gmail.com']
send_mail(subject, message, from_email, recipient_list)
