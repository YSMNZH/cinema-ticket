from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import CustomUser
import re
import datetime


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['name', 'family_name', 'username', 'email', 'phone_number', 'date_birth', 'password']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Enter a valid email address.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not re.match(r'^\d{11}$', phone_number):
            raise ValidationError("Phone number must be 11 digits.")
        return phone_number

    def clean_date_birth(self):
        date_birth = self.cleaned_data.get("date_birth")
        if date_birth and date_birth > datetime.date.today():
            raise ValidationError("Birth date cannot be in the future.")
        return date_birth

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one letter and one number.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise ValidationError("Passwords do not match.")
        return cleaned_data

class CustomUserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")        
        return cleaned_data