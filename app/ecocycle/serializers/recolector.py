from rest_framework import serializers
from ..models.recolector import Recolector

class RecolectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recolector
        fields = ['id', 'email']