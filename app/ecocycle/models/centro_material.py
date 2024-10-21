from django.db import models

class CentroMaterial(models.Model):
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    centro = models.ForeignKey('Centro', on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'centro_material'
        unique_together = ['material', 'centro']
    
    def __str__(self):
        return f"{self.centro}: {self.material} y cantidad {self.cantidad}"