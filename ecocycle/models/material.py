from django.db import models

class Material(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'material'

    def __str__(self) -> str:
        return self.nombre
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
        }