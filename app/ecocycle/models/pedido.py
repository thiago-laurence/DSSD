from django.db import models
from django.utils import timezone

class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    deposito = models.ForeignKey('Deposito', on_delete=models.PROTECT, null=False, blank=False)
    centro = models.ForeignKey('Centro', on_delete=models.PROTECT, null=True, blank=True)
    material = models.OneToOneField('Material', on_delete=models.PROTECT, null=False, blank=False)
    cantidad = models.IntegerField(null=False, blank=False)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'pedido'

    def __str__(self):
        return f'Pedido {self.id} [{self.fecha}] - {self.id_global}. Material: {self.material} ({self.cantidad})'
    