from decimal import Decimal
from django.shortcuts import redirect, render
from django.contrib import messages
from rest_framework.decorators import api_view
from ecocycle.models.punto import Punto
from ecocycle.models.material import Material
from ecocycle.models.centro import Centro
from ecocycle.helpers.auth import login_required

@api_view(['GET'])
@login_required(subclase='administrador')
def index(request):
    if 'user' not in request.session or request.session['user']['subclase'] != 'administrador':
        return redirect('login:index')
    
    return render(request, 'administrador/index.html')

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