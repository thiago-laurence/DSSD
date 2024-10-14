from django.db import models
from .lugar import Lugar

class Punto(Lugar):
    materiales = models.ManyToManyField('Material', related_name='puntos', blank=True)

    def to_dict(self):
        dict = super().to_dict()
        dict['materiales'] = [material.to_dict() for material in self.materiales.all()]
        
        return dict