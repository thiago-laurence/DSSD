from django.db import models

class Recoleccion(models.Model):
    materiales = models.ManyToManyField('Material', through='RecoleccionMaterial')
    recolector = models.ForeignKey('Recolector', related_name='recolecciones', on_delete=models.CASCADE)
    semana = models.DateField()
    pago = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(max_length=250)
    
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
        }