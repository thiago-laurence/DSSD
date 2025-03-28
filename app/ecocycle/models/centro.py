from django.db import models
from .lugar import Lugar
from ecocycle.models.centro_material import CentroMaterial
class Centro(Lugar):
    materiales = models.ManyToManyField('Material', through='CentroMaterial')
    
    def to_dict(self):
        dict = super().to_dict()
        dict['materiales'] = [
            {
                'nombre': cm.material.nombre,
                'cantidad': str(cm.cantidad),
            } for cm in self.centromaterial_set.all()
        ]
        
        return dict
    
    def has_enough_material(self, material, cantidad):
        if material in self.materiales.all():
            centro_material = CentroMaterial.objects.get(material=material, centro=self)
            
            if centro_material.cantidad >= cantidad:
                centro_material.cantidad -= cantidad
                centro_material.save()
                return True
        else:
            return False