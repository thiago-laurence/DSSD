from decimal import Decimal
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
from ..models.centro import Centro
from ..serializers.centro import CentroSerializer
from ..serializers.recolector import RecolectorSerializer
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
    try:
        cantidad = Decimal(cantidad)
    except:
        return JsonResponse({"error": "Cantidad debe ser un número decimal."}, status=status.HTTP_400_BAD_REQUEST)
    
    pedido = Pedido.objects.create(
        deposito=deposito,
        material=material,
        cantidad=cantidad
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
        return JsonResponse({"error": "Cantidad debe ser un número decimal."}, status=status.HTTP_400_BAD_REQUEST)

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
def asignar_pedido(request):
    pedido_id = request.POST.get('pedido_id')
    if pedido_id:
        pedido = Pedido.objects.get(id=pedido_id)
        centro_asignado = Centro.objects.get(id=request.session['user']['id'])
        hay_materiales = centro_asignado.has_enough_material(pedido.material, pedido.cantidad)
        if hay_materiales:
            pedido.centro = centro_asignado
            pedido.save()
            return JsonResponse({"message": "Pedido tomado correctamente."}, status=200)
        else: 
            return JsonResponse({"error": "No hay suficiente material en el centro de acopio."}, status=400)
    else:
        return JsonResponse({"error": "ID de pedido no proporcionado."}, status=400)

@csrf_exempt
@api_view(['POST'])
def add_deposito(request):
    nombre = request.data.get('nombre')
    direccion = request.data.get('direccion')
    email = request.data.get('email')
    password = request.data.get('password')

    if not nombre or not direccion or not email or not password:
        return JsonResponse({"error": "Nombre, dirección, email y password son campos obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        deposito = Deposito.objects.create( nombre=nombre, direccion=direccion, email=email, password=password)
    except Exception as e:
        return JsonResponse({"error": "El email del deposito ya fue registrado."}, status=status.HTTP_409_CONFLICT)
    
    return JsonResponse({"message": 'El deposito fue registrado correctamente'}, status=status.HTTP_201_CREATED)