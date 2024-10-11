from rest_framework import serializers
from ..models.deposito import Deposito

class DepositoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposito
        fields = ['id', 'email', 'nombre']