from django.db import models
from django.utils import timezone

class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    id_global = models.IntegerField(unique=True)
    id_local = models.IntegerField(unique=True)
    material = models.ForeignKey('Material', on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'pedido'

    def __str__(self):
        return f'Pedido {self.id} [{self.fecha}] - {self.id_global}. Material: {self.material} ({self.cantidad})'
    