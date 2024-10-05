from decimal import Decimal
from django.shortcuts import render, redirect
from . import api_views
from django.http import JsonResponse
from ..models.material import Material
from ..models.recolector import Recolector
from ..models.recoleccion import Recoleccion
from ..models.recoleccion_material import RecoleccionMaterial
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date
from django.http import HttpResponseBadRequest
from django.db import IntegrityError, transaction
from urllib.parse import parse_qs
from django.contrib import messages

def index(request):
    if 'user' not in request.session:
        return redirect('login:index')
    return render(request, 'materials/index.html')

def send(request):
    api_views.obtener_procesos(request)
    if request.method == 'POST':
        _obtener_recoleccion(request)
        if request.POST.get('finalize_process') != 'on':
            return render(request, 'materials/index.html')
        else:
            return redirect('/')
    return redirect('/')

@csrf_exempt
def _obtener_recoleccion(request):
    if request.method == 'POST':
        try:
            request_body = request.body.decode('utf-8')  # Decode bytes to string
            parsed_data = parse_qs(request_body)
            json_data = {key: value[0] for key, value in parsed_data.items()}
            json_string = json.dumps(json_data)
            body = json.loads(json_string)
            material_nombre = body.get('material')
            cantidad = Decimal(body.get('cantidad'))
            
            if not material_nombre or not cantidad or material:
                messages.error(request, "Error: Se debe indicar un material y una cantidad.")
                return HttpResponseBadRequest("Material and quantity must be provided.")

            recolector_id = request.session['user'].get('id')  # Assuming 'user_id' is stored in the session
            recolector = Recolector.objects.filter(id=recolector_id).first()

            if not recolector:
                messages.error(request, "Error: Error al recuperar recolección de usuario.")
                return HttpResponseBadRequest("Recolector not found.")
            
            material = Material.objects.filter(nombre=material_nombre).first()
            if not material:
                messages.error(request, "Error: El material indicado no existe.")
                return HttpResponseBadRequest(f"Material '{material_nombre}' does not exist.")
            
            with transaction.atomic():
                # Check if there's an existing Recoleccion for this user today
                recoleccion, created = Recoleccion.objects.get_or_create(
                    recolector=recolector,
                    semana=date.today(),
                    defaults={
                        'pago': Decimal(0.0),
                        'observaciones': 'Ninguna',
                        'aprobada': False
                    }
                )

                # Create a new RecoleccionMaterial
                RecoleccionMaterial.objects.create(
                    material=material,
                    recoleccion=recoleccion,
                    cantidad=cantidad
                )

                # Update payment
                recoleccion.pago += material.precio * cantidad
                recoleccion.save()

            messages.success(request, "Material de recolección procesado con éxito.")
            return JsonResponse({"message": "Recoleccion successfully processed."})
        
        except json.JSONDecodeError as e:
            print("Invalid JSON Format")
            messages.error(request, "Error: Formulario con formato incorrecto. Vuelva a intentarlo.")
            return HttpResponseBadRequest("Invalid JSON data.")
        
        except IntegrityError as e:
            print(f"IntegrityError: {str(e)}")
            messages.error(request, f"Error: Material ya ingresado en la recolección de hoy.")
            return HttpResponseBadRequest(f"IntegrityError: {str(e)}")
        
        except Exception as e:
            print(f"Error processing the request: {str(e)}")
            messages.error(request, f"Ocurró un error. Contacte un administrador.")
            return HttpResponseBadRequest(f"Error processing the request: {str(e)}")
    
    print("Invalid request method.")
    messages.error(request, f"Ocurró un error. Contacte un administrador.")
    return HttpResponseBadRequest(f"Invalid request method: {str(e)}")
    