from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, phone, email=None, username=None, password=None):
        if not phone:
            raise ValueError('Users must have a phone number')
        user = self.model(phone=phone, email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']
