from django.db import models
from .managers.user import CustomUser

class Usuario(CustomUser):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    username = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.nombre + ' ' + self.apellido
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f"{self.nombre}.{self.apellido}"
        super().save(*args, **kwargs)
    
    def to_dict(self):
        dict = super().to_dict()
        dict['nombre'] = self.nombre + ' ' + self.apellido
        
        return dict