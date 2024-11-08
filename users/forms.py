# accounts/forms.py
from django import forms

class LoginForm(forms.Form):
    identifier = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'placeholder': 'Email, Phone, or Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
