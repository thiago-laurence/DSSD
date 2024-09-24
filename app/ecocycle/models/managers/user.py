from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .user_manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    subclase = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email + ' ' + self.subclase

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
            self.subclase = self.__class__.__name__.lower()
        return super().save(*args, **kwargs)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'subclase': self.subclase
        }