from django.contrib.auth.hashers import make_password
from django.db import models

class Lugar(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    direccion = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.contraseña = make_password(self.contraseña)
        return super().save(*args, **kwargs)