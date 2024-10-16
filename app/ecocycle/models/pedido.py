from django.db import models
from django.utils import timezone

class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    deposito = models.ForeignKey('Deposito', on_delete=models.PROTECT, null=False, blank=False)
    centro = models.ForeignKey('Centro', on_delete=models.PROTECT, null=True, blank=True)
    material = models.ForeignKey('Material', on_delete=models.PROTECT, null=False, blank=False)
    cantidad = models.IntegerField(null=False, blank=False)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_solicitada = models.DateTimeField(default=None, null=True, blank=True)
    fecha_reserva = models.DateTimeField(default=None, null=True, blank=True)
    fecha_envio = models.DateTimeField(default=None, null=True, blank=True)

    class Meta:
        db_table = 'pedido'
        constraints = [
            models.UniqueConstraint(fields=['deposito', 'material', 'fecha_creacion'],   name='unique_deposito_material_fecha-creacion',)
        ]

    def __str__(self):
        return f'Pedido {self.id} [{self.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")}] - Deposito {self.deposito} Centro {self.centro}. Material: {self.material} ({self.cantidad})'