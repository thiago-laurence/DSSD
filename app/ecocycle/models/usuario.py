from django.contrib.auth.hashers import make_password
from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.nombre + ' ' + self.apellido
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.contraseña = make_password(self.contraseña)
        return super().save(*args, **kwargs)