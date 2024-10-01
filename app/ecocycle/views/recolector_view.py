from django.shortcuts import redirect, render, get_list_or_404
from rest_framework.decorators import api_view
from ecocycle.models.recoleccion import Recoleccion

@api_view(['GET'])
def index(request):
    if 'user' not in request.session:
        return redirect('login:index')
    
    return render(request, 'recolector/index.html')

@api_view(['GET'])
def view_recolecciones(request, id_recolector):
    if 'user' not in request.session:
        return redirect('login:index')
    
    recolecciones = get_list_or_404(Recoleccion, recolector=id_recolector)
    context = {
        'recolecciones': [recoleccion.to_dict_info() for recoleccion in recolecciones],
    }
    
    return render(request, 'recolector/recolecciones.html', { 'context': context })

@api_view(['POST'])
def close_recoleccion(request, id_recoleccion):
    if 'user' not in request.session:
        return redirect('login:index')
    
    recoleccion = Recoleccion.objects.get(id=id_recoleccion)
    recoleccion.notificacion = False
    request.session['user']['notificacion'] -= 1
    request.session.modified = True
    recoleccion.save()
    
    return redirect('recolector:view_recolecciones', id_recolector=recoleccion.recolector.id)