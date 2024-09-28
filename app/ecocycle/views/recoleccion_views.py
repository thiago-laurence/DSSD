from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from ecocycle.models.recoleccion import Recoleccion

@api_view(['GET'])
def view_recoleccion(request, id_recoleccion):
    if 'user' not in request.session:
        return redirect('login:index')
    
    recoleccion = Recoleccion.objects.get(id=id_recoleccion)
    context = {
        'recoleccion': recoleccion.to_dict(),
    }
    
    return render(request, 'recoleccion/view.html', { 'context': context })

@api_view(['POST'])
def update_recoleccion(request):
    if 'user' not in request.session:
        return redirect('login:index')
    print(request.data)
    recoleccion = Recoleccion.objects.filter(id=request.data.get('id_recoleccion')).first()
    if not recoleccion:
        return redirect('centro:index')
    
    recoleccion.observaciones = request.data.get('observaciones')
    recoleccion.save()
    
    return redirect('recoleccion:view', id_recoleccion=recoleccion.id)