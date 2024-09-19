from django.contrib.auth.hashers import make_password
from django.db import models
from .managers.user import CustomUser

class Usuario(CustomUser):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.nombre + ' ' + self.apellido
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        return super().save(*args, **kwargs)