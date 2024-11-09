from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    identifier = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'placeholder': 'Email, Phone, or Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


from django import forms
from .models import User

# users/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.core import validators
from .models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password']

    # Custom validation for email
# users/forms.py

def clean_email(self):
    email = self.cleaned_data.get('email')
    if email is None:
        raise ValidationError("Email is required")
    try:
        EmailValidator()(email)
    except ValidationError:
        raise ValidationError("Invalid email format")
    if User.objects.filter(email=email).exists():
        raise ValidationError("Email is already in use")
    return email

# users/forms.py

def clean_password(self):
    password = self.cleaned_data.get('password')
    if password is None:
        raise ValidationError("Password is required")
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must contain at least one digit")
    if not any(char.isalpha() for char in password):
        raise ValidationError("Password must contain at least one letter")
    if not any(char in "!@#$%^&*()-_+=<>?" for char in password):
        raise ValidationError("Password must contain at least one special character")
    return password

# users/forms.py

def clean_username(self):
    username = self.cleaned_data.get('username')
    if username is None:
        raise ValidationError("Username is required")
    if len(username) < 3:
        raise ValidationError("Username must be at least 3 characters long")
    if User.objects.filter(username=username).exists():
        raise ValidationError("Username is already taken")
    return username
# users/forms.py

def clean_phone(self):
    phone = self.cleaned_data.get('phone')
    if phone is None:
        raise ValidationError("Phone number is required")
    if len(phone) != 11:
        raise ValidationError("Phone number must be exactly 11 digits long")
    if not phone.startswith('09'):
        raise ValidationError("Phone number must start with '09'")
    if User.objects.filter(phone=phone).exists():
        raise ValidationError("Phone number is already in use")
    return phone

    # Custom validation for password confirmation
    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise ValidationError("Passwords do not match")
        return password_confirmation

