from django.db import models
from .usuario import Usuario
from .recoleccion import Recoleccion

class Recolector(Usuario):
    puntos = models.ManyToManyField('Punto', related_name='recolectores', blank=True)

    def to_dict(self, all=True):
        dict = super().to_dict()
        if all:
            dict['puntos'] = list(self.puntos.values('id', 'nombre', 'direccion'))
            dict['notificacion'] = self.recolecciones.filter(notificacion=True).count()
        
        return dict