from decimal import Decimal
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect, render, get_list_or_404
from rest_framework.decorators import api_view
from ecocycle.models.recoleccion import Recoleccion
from ecocycle.models.recoleccion_material import RecoleccionMaterial
from ecocycle.models.material import Material

@api_view(['GET'])
def index(request):
    if 'user' not in request.session or request.session['user']['subclase'] != 'recolector':
        return redirect('login:index')
    
    context = {
        'materiales': Material.objects.all(),
    }

    try:
        recoleccion = Recoleccion.objects.filter(recolector=request.session['user']['id']).latest('semana')
        fecha_actual = timezone.now().date()
        semana_actual = fecha_actual.isocalendar()[1]
        semana_recoleccion = recoleccion.semana.isocalendar()[1]
        if semana_recoleccion == semana_actual:
            context['recoleccion'] = recoleccion.to_dict_info()
            context['materiales'] = [m for m in context['materiales'] if m not in recoleccion.materiales.all()]
    except Recoleccion.DoesNotExist:
        recoleccion = None
    
    return render(request, 'recolector/index.html', { 'context': context })

@api_view(['GET'])
def view_recolecciones(request, id_recolector):
    if 'user' not in request.session:
        return redirect('login:index')
    
    recolecciones = Recoleccion.objects.filter(recolector=id_recolector)
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

@api_view(['POST'])
def add_recoleccion(request):
    if 'user' not in request.session:
        return redirect('login:index')
    
    if not request.POST.get("material"):
        messages.error(request, "Debe seleccionar un material válido.")
        return redirect('recolector:index')
    
    material = Material.objects.get(id=request.POST.get("material"))
    if request.POST.get("id_recoleccion"):
        recoleccion = Recoleccion.objects.get(id=request.POST.get("id_recoleccion"))
    else:
        recoleccion = Recoleccion.objects.create(recolector_id=request.session['user']['id'])
    rm = RecoleccionMaterial.objects.create(recoleccion=recoleccion, material=material, cantidad=Decimal(request.POST.get("cantidad")))
    
    recoleccion.pago += material.precio * rm.cantidad
    recoleccion.materiales.add(material)
    
    materiales = [m for m in Material.objects.all() if m not in recoleccion.materiales.all()]
    if request.POST.get("finalize_process") or (not materiales):
        recoleccion.finalizada = True
    
    recoleccion.save()

    return redirect('recolector:index')