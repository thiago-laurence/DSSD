import datetime
from decimal import Decimal
from django.db import models

class Recoleccion(models.Model):
    materiales = models.ManyToManyField('Material', through='RecoleccionMaterial')
    recolector = models.ForeignKey('Recolector', related_name='recolecciones', on_delete=models.CASCADE)
    semana = models.DateField(default=datetime.date.today)
    pago = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.0))
    observaciones = models.TextField(max_length=250, default='')
    finalizada = models.BooleanField(default=False)
    notificacion = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'recoleccion'
    
    def __str__(self) -> str:
        return f'Recoleccion {self.id}'
    
    def to_dict(self):
        return {
            'id': self.id,
            'recolector': self.recolector.to_dict(all=False),
            'materiales': [
                {
                    'material': material.to_dict(),
                    'cantidad': material.recoleccionmaterial_set.get(recoleccion=self).cantidad
                } for material in self.materiales.all()
            ],
            'semana': self.semana,
            'pago': self.pago,
            'observaciones': self.observaciones,
            'finalizada': self.finalizada,
            'notificacion': self.notificacion
        }
    
    def to_dict_info(self):
        dict = self.to_dict()
        del dict['recolector']
        
        return dict