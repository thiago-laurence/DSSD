from django import models

class MaterialRecoleccion(models.Model):
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    recoleccion = models.ForeignKey('Recoleccion', on_delete=models.CASCADE)
    cantidad = models.FloatField()
    
    class Meta:
        db_table = 'material_recoleccion'
    
    def __str__(self) -> str:
        return f'MaterialRecoleccion {self.id}'