from django.db import models

class Recoleccion(models.Model):
    materiales = models.ManyToManyField('Material', through='RecoleccionMaterial')
    semana = models.DateField()
    pago = models.FloatField()
    observaciones = models.TextField()
    
    class Meta:
        db_table = 'recoleccion'
    
    def __str__(self) -> str:
        return f'Recoleccion {self.id}'