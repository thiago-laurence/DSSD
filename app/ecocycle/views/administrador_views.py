from decimal import Decimal
from django.db.models import Sum, Count, Q, F
from django.shortcuts import redirect, render
from django.contrib import messages
from rest_framework.decorators import api_view
from ecocycle.models.punto import Punto
from ecocycle.models.pedido import Pedido
from ecocycle.models.material import Material
from ecocycle.models.centro import Centro
from ecocycle.models.recolector import Recolector
from ecocycle.models.recoleccion_material import RecoleccionMaterial
from ecocycle.helpers.auth import login_required

@api_view(['GET'])
@login_required(subclase='administrador')
def index(request):
    context = {
        'materiales': Material.objects.all().order_by('nombre'),
    }

    email_recolector = request.GET.get('email_recolector', '')
    if email_recolector: 
        if Recolector.objects.filter(email=email_recolector).exists():
            context['mvp_recolector'] = Recolector.objects.filter(email=email_recolector).annotate(
                total_materiales=Sum('recolecciones__recoleccionmaterial__cantidad_real'),
                cantidad_recolecciones=Count('recolecciones', distinct=True)
            ).first()
        else: messages.error(request, "No existe un recolector con el email ingresado")
    else: context['mvp_recolector'] = Recolector.objects.annotate(
                total_materiales=Sum('recolecciones__recoleccionmaterial__cantidad_real'),
                cantidad_recolecciones=Count('recolecciones', distinct=True)
            ).filter(total_materiales__isnull=False).order_by('-total_materiales').first()
    
    id_material = request.GET.get('material', '')
    if id_material: 
        if Material.objects.filter(id=id_material).exists():
            context['mvp_material'] = Material.objects.filter(id=id_material).annotate(
                total_materiales=Sum('recoleccionmaterial__cantidad_real'),
                cantidad_recolecciones=Count('recoleccionmaterial', distinct=True)
            ).first()
        else: messages.error(request, "No existe el material seleccionado")
    else: context['mvp_material'] = Material.objects.annotate(
                total_materiales=Sum('recoleccionmaterial__cantidad_real'),
                cantidad_recolecciones=Count('recoleccionmaterial', distinct=True)
            ).filter(total_materiales__isnull=False).order_by('-total_materiales').first()
    
    result = Pedido.objects.aggregate(
        pedidos_con_centro=Count('id', filter=~Q(centro=None)),
        total_pedidos=Count('id')
    )
    context['promedio_pedidos'] = (
        (result['pedidos_con_centro'] / result['total_pedidos']) * 100 
        if result['total_pedidos'] > 0 else 0
    )

    result = RecoleccionMaterial.objects.aggregate(
        recolecciones_coincidentes=Count('id', filter=Q(cantidad_recolectada=F('cantidad_real'))),
        total_recolecciones=Count('id')
    )
    context['promedio_pedidos_sin_diferencias'] = (
        (result['recolecciones_coincidentes'] / result['total_recolecciones']) * 100
        if result['total_recolecciones'] > 0 else 0
    )

    result = Pedido.objects.filter(centro__isnull=False).aggregate(
        pedidos_a_tiempo=Count('id', filter=Q(fecha_envio__lt=F('fecha_solicitada'))),
        total_pedidos=Count('id')
    )
    context['promedio_pedidos_a_tiempo'] = (
        (result['pedidos_a_tiempo'] / result['total_pedidos']) * 100
        if result['total_pedidos'] > 0 else 0
    )

    return render(request, 'administrador/index.html', {'context': context })

@api_view(['GET'])
@login_required(subclase='administrador')
def view_puntos(request):
    context = {
        'puntos': [ p.to_dict() for p in Punto.objects.all().order_by('nombre')],
        'materiales': Material.objects.all().order_by('nombre')
    }
    
    return render(request, 'administrador/puntos.html', {'context': context })

@api_view(['POST'])
@login_required(subclase='administrador')
def add_punto(request):
    if 'materiales' not in request.POST:
        messages.error(request, "Debe seleccionar al menos un material")
        return redirect('administrador:puntos')
    
    nombre = request.POST['nombre']
    direccion = request.POST['direccion']
    email = request.POST['email']
    password = request.POST['password']

    try:
        punto = Punto.objects.create(nombre=nombre, direccion=direccion, email=email, password=password)
        materiales_ids = request.POST.getlist('materiales')
        materiales = Material.objects.filter(id__in=materiales_ids)
        punto.materiales.add(*materiales)
    except Exception as e:
        messages.error(request, "El nombre o email ingresado ya se encuentra registrado")
    
    return redirect('administrador:puntos')

@api_view(['GET'])
@login_required(subclase='administrador')
def view_centros(request):
    context = {
        'centros': [ c.to_dict() for c in Centro.objects.all().order_by('nombre')],
    }

    return render(request, 'administrador/centros.html', {'context': context })

@api_view(['POST'])
@login_required(subclase='administrador')
def add_centro(request):
    nombre = request.POST['nombre']
    direccion = request.POST['direccion']
    email = request.POST['email']
    password = request.POST['password']
    try:
        Centro.objects.create(nombre=nombre, direccion=direccion, email=email, password=password)
    except Exception as e:
        messages.error(request, "El nombre o email ingresado ya se encuentra registrado")
    
    return redirect('administrador:centros')

@api_view(['GET'])
@login_required(subclase='administrador')
def view_materiales(request):
    context = {
        'materiales': Material.objects.all().order_by('nombre')
    }
    return render(request, 'administrador/materiales.html', {'context': context })

@api_view(['POST'])
@login_required(subclase='administrador')
def add_material(request):
    nombre = request.POST['nombre'].lower().capitalize()
    precio = Decimal(request.POST['precio'])
    try:
        Material.objects.create(nombre=nombre, precio=precio)
    except Exception as e:
        messages.error(request, "El material ingresado ya se encuentra registrado")
    
    return redirect('administrador:materiales')

@api_view(['GET'])
@login_required(subclase='administrador')
def view_recolectores(request):
    context = {
        'recolectores': [ r.to_dict() for r in Recolector.objects.all().order_by('email')],
        'puntos': [ p.to_dict(all=False) for p in Punto.objects.all().order_by('nombre') ]
    }

    return render(request, 'administrador/recolectores.html', {'context': context })

@api_view(['POST'])
@login_required(subclase='administrador')
def add_recolector(request):
    nombre = request.POST['nombre'].lower().capitalize()
    apellido = request.POST['apellido'].lower().capitalize()
    email = request.POST['email'].lower()
    password = request.POST['password']
    if 'puntos' not in request.POST:
        messages.error(request, "Debe seleccionar al menos un punto de recolección")
        return redirect('administrador:recolectores')

    try:
        recolector = Recolector.objects.create(nombre=nombre, apellido=apellido, email=email, password=password)
        puntos_ids = request.POST.getlist('puntos')
        puntos = Punto.objects.filter(id__in=puntos_ids)
        recolector.puntos.add(*puntos)
    except Exception as e:
        messages.error(request, "El email ingresado ya se encuentra registrado")
    
    return redirect('administrador:recolectores')