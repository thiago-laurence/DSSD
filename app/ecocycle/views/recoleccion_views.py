from django.shortcuts import redirect, render, get_object_or_404
from rest_framework.decorators import api_view
from ecocycle.models.recoleccion import Recoleccion
from ecocycle.models.centro import Centro
from ecocycle.models.centro_material import CentroMaterial

@api_view(['GET'])
def view_recoleccion(request, id_recoleccion):
    if 'user' not in request.session:
        return redirect('login:index')
    
    recoleccion = get_object_or_404(Recoleccion, id=id_recoleccion)
    context = {
        'recoleccion': recoleccion.to_dict(),
    }
    
    return render(request, 'recoleccion/view.html', { 'context': context })

@api_view(['POST'])
def update_recoleccion(request):
    if 'user' not in request.session:
        return redirect('login:index')
    
    recoleccion = get_object_or_404(Recoleccion, id=request.data.get('id_recoleccion'))
    
    recoleccion.observaciones = request.data.get('observaciones')
    recoleccion.aprobada = True
    recoleccion.notificacion = True
    centro = Centro.objects.get(id=request.session['user']['id'])
    
    for rm in recoleccion.recoleccionmaterial_set.all():
        try:
            centro_material = CentroMaterial.objects.get(centro=request.session['user']['id'], material=rm.material)
            centro_material.cantidad += rm.cantidad
            centro_material.save()
        except CentroMaterial.DoesNotExist:
            CentroMaterial.objects.create(centro=centro, material=rm.material, cantidad=rm.cantidad)
    
    recoleccion.save()
    
    return redirect('recoleccion:view', id_recoleccion=recoleccion.id)