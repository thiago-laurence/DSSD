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
from django.db import transaction
from urllib.parse import parse_qs

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
            
            if not material_nombre or not cantidad:
                #print("Material or quantity missing in the request")
                return HttpResponseBadRequest("Material and quantity must be provided.")

            recolector_id = request.session['user'].get('id')  # Assuming 'user_id' is stored in the session
            recolector = Recolector.objects.filter(id=recolector_id).first()

            if not recolector:
                #print("Recolector not found.")
                return HttpResponseBadRequest("Recolector not found.")
            
            #print(f"Recolector: {recolector}")

            material = Material.objects.filter(nombre=material_nombre).first()
            if not material:
                #print(f"Material '{material_nombre}' does not exist.")
                return HttpResponseBadRequest(f"Material '{material_nombre}' does not exist.")
            
            with transaction.atomic():
                # Check if there's an existing Recoleccion for this user today
                #print("Checking for existing Recoleccion")
                recoleccion, created = Recoleccion.objects.get_or_create(
                    recolector=recolector,
                    semana=date.today(),
                    defaults={
                        'pago': Decimal(0.0),
                        'observaciones': 'Ninguna',
                        'aprobada': False
                    }
                )
                
                #if created:
                #    print("New Recoleccion created.")
                #else:
                #    print("Existing Recoleccion found.")

                # Create a new RecoleccionMaterial
                #print(f"Creating RecoleccionMaterial for material {material.nombre} and cantidad {cantidad}")
                RecoleccionMaterial.objects.create(
                    material=material,
                    recoleccion=recoleccion,
                    cantidad=cantidad
                )

                # Update payment
                #print(f"Updating Recoleccion payment by adding {material.precio * cantidad}")
                recoleccion.pago += material.precio * cantidad
                recoleccion.save()

            #print("Recoleccion successfully processed.")
            return JsonResponse({"message": "Recoleccion successfully processed."})
        
        except json.JSONDecodeError as e:
            print("Invalid JSON data.")
            return HttpResponseBadRequest("Invalid JSON data.")
        
        except Exception as e:
            print(f"Error processing the request: {str(e)}")
            return HttpResponseBadRequest(f"Error processing the request: {str(e)}")
    
    print("Invalid request method.")
    return HttpResponseBadRequest("Invalid request method.")
    