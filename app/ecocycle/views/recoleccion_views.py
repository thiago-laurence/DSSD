from decimal import Decimal
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework.decorators import api_view
from ecocycle.models.recoleccion import Recoleccion
from ecocycle.models.centro import Centro
from ecocycle.models.centro_material import CentroMaterial
from ecocycle.helpers.auth import login_required
from ecocycle.views.bonita_views import consolidacion_materiales_entregados

@api_view(['GET'])
@login_required(subclase='centro')
def view_recoleccion(request, id_recoleccion):
    recoleccion = get_object_or_404(Recoleccion, id=id_recoleccion)
    context = {
        'recoleccion': recoleccion.to_dict(),
    }
    
    return render(request, 'recoleccion/view.html', { 'context': context })

@api_view(['POST'])
@login_required(subclase='centro')
def update_recoleccion(request):
    recoleccion = get_object_or_404(Recoleccion, id=request.POST.get('id_recoleccion'))
    cantidad_real = request.POST.getlist('cantidad_real')
    recoleccion.observaciones = request.POST.get('observaciones')
    recoleccion.notificacion = True
    recoleccion.finalizada = True
    recoleccion.pago = Decimal(0.0)

    centro = Centro.objects.get(id=request.session['user']['id'])
    i = 0
    for rm in recoleccion.recoleccionmaterial_set.all().order_by('id'):
        try:
            rm.cantidad_real = Decimal(cantidad_real[i])
            recoleccion.pago += rm.material.precio * rm.cantidad_real
            centro_material = centro.centromaterial_set.get(material=rm.material)
            centro_material.cantidad += rm.cantidad_real
            centro_material.save()
        except CentroMaterial.DoesNotExist:
            CentroMaterial.objects.create(centro=centro, material=rm.material, cantidad=rm.cantidad_real)
        rm.save()
        i += 1
    recoleccion.save()
    request.session.modified = True
    consolidacion_materiales_entregados(request)
    
    return redirect('recoleccion:view', id_recoleccion=recoleccion.id)