import random
from decimal import Decimal
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from ..models.deposito import Deposito
from ..models.pedido import Pedido
from ..models.material import Material
from ..models.centro import Centro
from ..serializers.centro import CentroSerializer
from ..serializers.pedido import PedidoSerializer

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
    fecha_solicitada = request.data.get('fecha_solicitada')

    try:
        cantidad = Decimal(cantidad)
    except:
        return JsonResponse({"error": "El campo Cantidad debe ser un número decimal."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        fecha_solicitada = datetime.strptime(fecha_solicitada, '%Y-%m-%d')
    except:
        return JsonResponse({"error": "El campo Fecha solicitada debe tener el formato YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    if fecha_solicitada <= datetime.now():
        return JsonResponse({"error": "La fecha solicitada debe ser posterior a la fecha de creación."}, status=status.HTTP_400_BAD_REQUEST)
    
    pedido = Pedido.objects.create(
        deposito=deposito,
        material=material,
        cantidad=cantidad,
        fecha_solicitada=fecha_solicitada
    )
    serializer = PedidoSerializer(pedido)

    return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_centros(request):
    if not request.GET.get('cantidad') or not request.GET.get('material'):
        return JsonResponse({"error": "Los campos Material y Cantidad son obligatorios"}, status=status.HTTP_400_BAD_REQUEST)
    
    material = get_object_or_404(Material, id=request.GET.get('material'))
    cantidad = request.GET.get('cantidad')
    try:
        cantidad = Decimal(cantidad)
    except:
        return JsonResponse({"error": "El campo Cantidad debe ser un número decimal."}, status=status.HTTP_400_BAD_REQUEST)

    centros = Centro.objects.all().filter(
        centromaterial__material=material,
        centromaterial__cantidad__gte=cantidad
    ).order_by('nombre')

    paginator = PageNumberPagination()
    paginator.page_size = 1
    result_page = paginator.paginate_queryset(centros, request)

    serializer = CentroSerializer(result_page, many=True)
    
    return paginator.get_paginated_response(serializer.data)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_deposito(request):
    nombre = request.data.get('nombre')
    direccion = request.data.get('direccion')
    email = request.data.get('email')
    password = request.data.get('password')

    if not nombre or not direccion or not email or not password:
        return JsonResponse({"error": "Nombre, dirección, email y password son campos obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        Deposito.objects.create( nombre=nombre, direccion=direccion, email=email, password=password)
    except Exception as e:
        return JsonResponse({"error": "El email del deposito ya fue registrado."}, status=status.HTTP_409_CONFLICT)
    
    return JsonResponse({"message": 'El deposito fue registrado correctamente'}, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['POST'])
def sorteo(request):
    deposito_id = int(request.data.get('deposito_id'))
    random_number = random.randint(1, 100)
    return JsonResponse({"random_number": random_number}, status=status.HTTP_200_OK)