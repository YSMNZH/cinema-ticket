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

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        
        if password != password_confirm:
            raise ValidationError("Passwords do not match.")
        return password_confirm
