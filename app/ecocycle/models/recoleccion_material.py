from django.db import models

class RecoleccionMaterial(models.Model):
    material = models.ForeignKey('Material', on_delete=models.PROTECT)
    recoleccion = models.ForeignKey('Recoleccion', on_delete=models.PROTECT)
    punto = models.ForeignKey('Punto', on_delete=models.PROTECT)
    cantidad_recolectada = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_real = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    class Meta:
        db_table = 'material_recoleccion'
        unique_together = ['material', 'recoleccion', 'punto']
    
    def __str__(self):
        return f"{self.recoleccion}: ({self.punto}) ({self.material})"