from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers.recolector import RecolectorSerializer
from ..models.pedido import Pedido

@api_view(['GET'])
def hello(request):
    return Response("Hello, world!", status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = RecolectorSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_pedidos(request):
    pedidos = Pedido.objects.all().values()
    return JsonResponse(list(pedidos), safe=False)