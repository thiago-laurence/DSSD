from rest_framework import serializers
from .deposito import DepositoSerializer
from .centro import CentroSerializer
from .material import MaterialSerializer
from ..models.pedido import Pedido

class PedidoSerializer(serializers.ModelSerializer):
    deposito = DepositoSerializer()
    centro = CentroSerializer()
    material = MaterialSerializer()

    class Meta:
        model = Pedido
        fields = ['id', 'deposito', 'centro', 'material', 'cantidad', 'fecha']