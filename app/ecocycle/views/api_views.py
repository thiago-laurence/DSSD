from django.http import JsonResponse
from ..models.pedido import Pedido
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def hello(request):
    return Response("Hello, world!", status=status.HTTP_200_OK)

@api_view(['GET'])
def get_pedidos(request):
    pedidos = Pedido.objects.all().values()
    return JsonResponse(list(pedidos), safe=False)