from django.http import JsonResponse

from ..models.deposito import Deposito
from ..models.pedido import Pedido
from ..models.material import Material
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import json

@api_view(['GET'])
def hello(request):
    return Response("Hello, world!", status=status.HTTP_200_OK)

@api_view(['GET'])
def get_pedidos(request):
    pedidos = Pedido.objects.all().values()
    return JsonResponse(list(pedidos), safe=False)

@csrf_exempt
def add_pedido(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            deposito_id = data['deposito']
            material_nombre = data['material']
            cantidad = data['cantidad']
            
            # Fetch Deposito object
            try:
                deposito = Deposito.objects.get(id=deposito_id)
            except Deposito.DoesNotExist:
                return JsonResponse({'error': 'Deposito not found'}, status=404)

            # Fetch Material object
            try:
                material = Material.objects.get(nombre=material_nombre)
            except Material.DoesNotExist:
                return JsonResponse({'error': 'Material not found'}, status=404)

            # Create the Pedido object
            pedido = Pedido.objects.create(
                deposito=deposito,
                centro=None,
                material=material,
                cantidad=cantidad
            )
            return JsonResponse({'message': 'Pedido created successfully', 'pedido_id': pedido.id}, status=201)

        except Material.DoesNotExist:
            return JsonResponse({'error': 'Material not found'}, status=404)
        except KeyError:
            return JsonResponse({'error': 'Invalid input data'}, status=400)
    else:
        return JsonResponse({'error': 'POST request required'}, status=405)