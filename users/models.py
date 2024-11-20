from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now
from django.db import models
from django.db import models
from datetime import timedelta

from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.conf import settings

def get_expiration_time():
    return now() + timedelta(minutes=20)

class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_expiration_time)

    def is_valid(self):
        return now() < self.expires_at

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, phone_number, password, **extra_fields)
    


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30, blank=True, null=True)
    family_name = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    date_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number', 'name', 'family_name', 'date_birth']

class PasswordResetTokens(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    token = models.CharField(max_length=255, unique=True, blank=True, null=True)
    expires_at = models.DateTimeField(default=get_expiration_time, blank=True, null=True)
    created_at = models.DateTimeField(default=now, blank=True, null=True)

    def __str__(self):
        return self.username
