from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from ecocycle.models.pedido import Pedido
from rest_framework.decorators import api_view
from ecocycle.models.recoleccion import Recoleccion
from ecocycle.models.recolector import Recolector
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
    pedidos = Pedido.objects.select_related('deposito',
     'centro', 'material').order_by('-fecha_creacion') # Lista de pedidos

    if pedidos:
        pedidos_sin_centro = [pedido for pedido in pedidos if pedido.centro is None]
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
            messages.error(request, 'No hay suficientes materiales para aceptar este pedido')
            return redirect('centro:list_pedidos')
    else:
        return render(request, 'centro/perfil.html')
    
@api_view(['GET'])
@login_required(subclase='centro')
def list_pedidos_aceptados(request):
    centro = get_object_or_404(Centro, id=request.session['user']['id'])
    pedidos = Pedido.objects.filter(centro=centro)

    if pedidos:
        pedidos_pendientes_envio = [pedido for pedido in pedidos if pedido.fecha_envio is None]
    else:
        pedidos_pendientes_envio = []
    
    
    paginator = Paginator(pedidos_pendientes_envio, 10)
    page_number = request.GET.get('page', 1)
    
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(1)
    
    context = {
        'pedidos': page.object_list,
        'page': page,
    }
    
    return render(request, 'centro/pedidos_aceptados.html', context)

@api_view(['POST'])
@login_required(subclase='centro')
def enviar_pedido(request):
    pedido_id = request.data.get('pedido_id')
    if pedido_id:
        pedido = get_object_or_404(Pedido, id=pedido_id)
        pedido.fecha_envio = timezone.now()
        pedido.save()
        
        return redirect('centro:pedidos_aceptados')
    else:
        return render(request, 'centro/perfil.html')

# @api_view(['GET'])
# @login_required(subclase='centro')
# def paginator(request):
#     page = int(request.GET.get('page', 1))
#     per_page = 2
    
#     users = Recolector.objects.order_by('email')
#     user_list = users.values('id', 'email', 'nombre', 'apellido')
#     paginator = Paginator(user_list, per_page)
#     try:
#         user_list = paginator.page(page)
#     except EmptyPage:
#         user_list = paginator.page(paginator.num_pages)
    
#     context = {
#         'user_list': list(user_list),
#         'page': page,
#         'per_page': per_page,
#         'page_range': range(1, paginator.num_pages + 1),
#         'view': 'centro:index'
#     }

#     return render(request, 'centro/index.html', { 'context': context })