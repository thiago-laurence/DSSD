from django import models

class MaterialRecoleccion(models.Model):
    material = models.ForeignKey('Material')
    recoleccion = models.ForeignKey('Recoleccion')
    cantidad = models.FloatField()
    
    class Meta:
        db_table = 'material_recoleccion'
    
    def __str__(self) -> str:
        return f'MaterialRecoleccion {self.id}'