import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from ..models.deposito import Deposito
from ..models.pedido import Pedido
from ..models.material import Material
from ..models.recolector import Recolector
from ..serializers.recolector import RecolectorSerializer
from ..serializers.pedido import PedidoSerializer

@api_view(['GET'])
def hello(request):
    return Response("Hello, world!", status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = RecolectorSerializer(request.user)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_users(request):
    users = Recolector.objects.all().order_by('email')
    paginator = PageNumberPagination()
    paginator.page_size = 1
    result_page = paginator.paginate_queryset(users, request)
    serializer = RecolectorSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha_creacion')
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(pedidos, request)
    serializer = PedidoSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_pedido(request):
    deposito = get_object_or_404(Deposito, id=request.data.get('deposito'))
    material = get_object_or_404(Material, nombre=request.data.get('material'))
    cantidad = request.data.get('cantidad')
    if isinstance(cantidad, str):
        return JsonResponse({'error': 'Cantidad must be an integer'}, status=status.HTTP_400_BAD_REQUEST)
    
    pedido = Pedido.objects.create(
        deposito=deposito,
        material=material,
        cantidad=cantidad
    )
    serializer = PedidoSerializer(pedido)

    return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
