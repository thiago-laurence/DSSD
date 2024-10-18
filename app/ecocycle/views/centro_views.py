from django.utils import timezone
import requests
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage
from ecocycle.models.pedido import Pedido
from rest_framework.decorators import api_view
from ecocycle.models.recoleccion import Recoleccion
from ecocycle.models.centro import Centro
from ecocycle.helpers.auth import login_required

@api_view(['GET'])
@login_required(subclase='centro')
def index(request):    
    id_recoleccion = request.GET.get('id_recoleccion', '')
    context = {
        'id_recoleccion': id_recoleccion,
        'error': False,
    }
    if id_recoleccion:
        if Recoleccion.objects.filter(id=id_recoleccion).exists():
            return redirect('recoleccion:view', id_recoleccion=id_recoleccion)
        
        context['error'] = True
        return render(request, 'centro/index.html', { 'context': context })
        
    return render(request, 'centro/index.html', { 'context': context })

@api_view(['GET'])
@login_required(subclase='centro')
def view_perfil(request):
    return render(request, 'centro/perfil.html')

@api_view(['GET'])
@login_required(subclase='centro')
def list_pedidos(request): 
    response = requests.get('http://localhost:8000/ecocycle/api/pedidos')
    pedidos = response.json().get('results') # Lista de pedidos
    print(pedidos)
    if pedidos:
        pedidos_sin_centro = [pedido for pedido in pedidos if pedido['centro'] is None]
    else:
        pedidos_sin_centro = []

    context = {
        'pedidos': pedidos_sin_centro
    }

    return render(request, 'centro/pedidos.html', context)

@api_view(['POST'])
@login_required(subclase='centro')
def asignar_pedido(request):
    pedido_id = request.data.get('pedido_id')
    if pedido_id:
        pedido = get_object_or_404(Pedido, id=pedido_id)
        centro_asignado = get_object_or_404(Centro, id=request.session['user']['id'])
        hay_materiales = centro_asignado.has_enough_material(pedido.material, pedido.cantidad)
        
        if hay_materiales:
            pedido.centro = centro_asignado
            pedido.fecha_reserva = timezone.now()
            pedido.save()
            
            return redirect('centro:list_pedidos') # Redirige a la lista de pedidos
        else: 
            return render(request, 'centro/perfil.html')
    else:
        return render(request, 'centro/perfil.html')