from rest_framework import serializers
from ..models.centro import Centro

class CentroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Centro
        fields = ['id', 'email', 'nombre']