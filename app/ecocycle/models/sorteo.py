from django.db import models

class Sorteo(models.Model):
    fecha = models.DateField()
    numero = models.IntegerField(unique=True)
    deposito = models.ForeignKey('Deposito', on_delete=models.PROTECT, related_name='sorteos')
    
    class Meta:
        db_table = 'sorteo'
    
    def __str__(self) -> str:
        return f'Sorteo: ID {self.id}'