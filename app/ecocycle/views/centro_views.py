from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage
from rest_framework.decorators import api_view
from ecocycle.models.recoleccion import Recoleccion
import requests

@api_view(['GET'])
def index(request):
    if 'user' not in request.session or request.session['user']['subclase'] != 'centro':
        return redirect('login:index')
    
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
def view_perfil(request, id_centro):
    if 'user' not in request.session:
        return redirect('login:index')
    
    return render(request, 'centro/perfil.html')

@api_view(['GET'])
def list_pedidos(request):
    if 'user' not in request.session:
        return redirect('login:index')
    
    response = requests.get('http://localhost:8000/ecocycle/api/pedidos')
    pedidos = response.json().get('results') # Lista de pedidos

    context = {
        'pedidos': pedidos
    }
    print(context['pedidos'][0])

    return render(request, 'centro/pedidos.html', context)