from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    # Define fields for password input and confirmation
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        # Include all required fields in the form
        fields = ['name', 'family_name', 'username', 'email', 'phone_number', 'date_birth', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # Check if passwords match
        if password != password_confirm:
            raise ValidationError("Passwords do not match.")
        
        # Additional validation logic if needed, e.g., age check for date_birth

        return cleaned_data

class CustomUserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        
        # Optional: You can add custom validation logic here (e.g., checking for a specific type of username)
        
        return cleaned_data