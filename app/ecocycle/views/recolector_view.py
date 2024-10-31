from decimal import Decimal
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from ecocycle.models.recolector import Recolector
from ecocycle.models.recoleccion import Recoleccion
from ecocycle.models.recoleccion_material import RecoleccionMaterial
from ecocycle.models.material import Material
from ecocycle.helpers.auth import login_required
from ecocycle.views.bonita_views import carga_material_recolectado

@api_view(['GET'])
@login_required(subclase='recolector')
def index(request):
    context = {
        'materiales': Material.objects.all(),
        'puntos': Recolector.objects.get(id=request.session['user']['id']).puntos.all(),
    }
    
    try:
        recoleccion = Recoleccion.objects.filter(recolector=request.session['user']['id']).latest('semana')
        fecha_actual = timezone.now().date()
        semana_actual = fecha_actual.isocalendar()[1]
        semana_recoleccion = recoleccion.semana.isocalendar()[1]
        if semana_recoleccion == semana_actual:
            context['recoleccion'] = recoleccion.to_dict_info()
    except Recoleccion.DoesNotExist:
        recoleccion = None

    return render(request, 'recolector/index.html', { 'context': context })

@api_view(['GET'])
@login_required(subclase='recolector')
def view_recolecciones(request, id_recolector):
    recolecciones = Recoleccion.objects.filter(recolector=id_recolector)
    context = {
        'recolecciones': [recoleccion.to_dict_info() for recoleccion in recolecciones],
    }
    
    return render(request, 'recolector/recolecciones.html', { 'context': context })

@api_view(['POST'])
@login_required(subclase='recolector')
def close_recoleccion(request, id_recoleccion):
    recoleccion = Recoleccion.objects.get(id=id_recoleccion)
    recoleccion.notificacion = False
    request.session['user']['notificacion'] -= 1
    request.session.modified = True
    recoleccion.save()
    
    return redirect('recolector:view_recolecciones', id_recolector=recoleccion.recolector.id)

@api_view(['POST'])
@login_required(subclase='recolector')
def add_recoleccion(request):
    if not request.POST.get("material"):
        messages.error(request, "Debe seleccionar un material válido.")
        return redirect('recolector:index')
    
    if not request.POST.get("punto"):
        messages.error(request, "Debe seleccionar un punto de recolección válido.")
        return redirect('recolector:index')

    material = Material.objects.get(id=request.POST.get("material"))
    punto = Recolector.objects.get(id=request.session['user']['id']).puntos.get(id=request.POST.get("punto"))
    if request.POST.get("id_recoleccion"):
        recoleccion = Recoleccion.objects.get(id=request.POST.get("id_recoleccion"))
    else:
        recoleccion = Recoleccion.objects.create(recolector_id=request.session['user']['id'])
    
    try:
        rm = RecoleccionMaterial.objects.create(recoleccion=recoleccion, material=material, punto=punto, cantidad_recolectada=Decimal(request.POST.get("cantidad_recolectada")))
    except Exception as e:
        messages.error(request, f"Ya posee una recoleccion del material {material.nombre} para el punto {punto.nombre}")
        return redirect('recolector:index')

    recoleccion.pago = material.precio * rm.cantidad_recolectada if recoleccion.pago is None else recoleccion.pago + (material.precio * rm.cantidad_recolectada)
    recoleccion.materiales.add(material)
    
    carga_material_recolectado(request) # Usa la API de Bonita
    if request.POST.get("finalize_task"):
        recoleccion.finalizada = True
    
    recoleccion.save()

    return redirect('recolector:index')