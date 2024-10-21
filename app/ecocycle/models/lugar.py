from django.db import models
from .managers.user import CustomUser

class Lugar(CustomUser):
    nombre = models.CharField(max_length=50, unique=True)
    direccion = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self.id} {self.__class__.__name__}'
    
    def to_dict(self):
        dict = super().to_dict()
        dict['nombre'] = self.nombre
        dict['direccion'] = self.direccion
        
        return dict