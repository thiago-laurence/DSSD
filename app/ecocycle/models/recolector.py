from django.db import models
from .usuario import Usuario

class Recolector(Usuario):
    puntos = models.ManyToManyField('Punto', related_name='recolectores', blank=True)

    def to_dict(self):
        dict = super().to_dict()
        dict['puntos'] = list(self.puntos.values('id', 'nombre', 'direccion'))
        
        return dict