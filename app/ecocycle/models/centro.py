from django.db import models
from .lugar import Lugar

class Centro(Lugar):
    materiales = models.ManyToManyField('Material', through='CentroMaterial')
    
    def to_dict(self):
        dict = super().to_dict()
        dict['materiales'] = [
            {
                'material': material.nombre,
                'cantidad': material.centromaterial_set.get(centro=self).cantidad
            } for material in self.materiales.all()
        ]
        
        return dict