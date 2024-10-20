from rest_framework import serializers
from ..models.centro_material import CentroMaterial

class CentroMaterialSerializer(serializers.ModelSerializer):
    # Sin esto no puedo obtener el nombre del material y la cantidad
    nombre = serializers.CharField(source='material.nombre')
    cantidad = serializers.IntegerField() 
    
    class Meta:
        model = CentroMaterial
        fields = ['nombre', 'cantidad']
