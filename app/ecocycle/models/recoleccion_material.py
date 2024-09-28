from django.db import models

class RecoleccionMaterial(models.Model):
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    recoleccion = models.ForeignKey('Recoleccion', on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'material_recoleccion'
        unique_together = ['material', 'recoleccion']
    
    def __str__(self):
        return f"{self.recoleccion}: {self.material} y cantidad {self.cantidad}"