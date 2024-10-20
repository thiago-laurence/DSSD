from rest_framework import serializers
from ..models.centro import Centro
from ..models.centro_material import CentroMaterial
from .centro_material import CentroMaterialSerializer

class CentroSerializer(serializers.ModelSerializer):
    materiales = serializers.SerializerMethodField() # Te permite definir como obtener los materiales de un centro
    class Meta:
        model = Centro
        fields = ['id', 'email', 'nombre', 'direccion', 'materiales']
    
    # Usa esta función para obtener los materiales de un centro
    def get_materiales(self, centro):
        centro_materiales = CentroMaterial.objects.filter(centro=centro)
        return CentroMaterialSerializer(centro_materiales, many=True).data