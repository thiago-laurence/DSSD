import json
from django.http import JsonResponse
import requests
from django.shortcuts import render
from os import environ as env
from ecocycle.models.recoleccion import Recoleccion

def index(request):
    obj = consolidacion_materiales_entregados(request)
    return render(request, 'api/index.html', {'obj': obj})

def login_bonita(request):
    url = "http://localhost:8080/bonita/loginservice"
    try:
        username = request.session['user']['email'].split('@')[0]
    except:
        username = request.data.get("email").split('@')[0]
    password = env.get("BONITA_PASS")
    
    payload = {
        "username": username,
        "password": password,
        "redirect": False
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200 or response.status_code == 204:
        jsessionid = response.cookies.get('JSESSIONID')
        x_bonita_api_token = response.cookies.get('X-Bonita-API-Token')

        request.session['bonita_tokens'] = {
            'X-Bonita-API-Token': x_bonita_api_token,
            'JSESSIONID': jsessionid   
        }

        return {
            'X-Bonita-API-Token': x_bonita_api_token,
            'JSESSIONID': jsessionid
        }

    else:
        return {}

def get_bonita_tokens(request):
    tokens = request.session.get('bonita_tokens')
    if not tokens:
        tokens = login_bonita(request)

    if not tokens: # Si dio error la autenticación con bonita, devuelvo None
        return {}
    
    headers = {
        "Cookie": f"JSESSIONID={tokens['JSESSIONID']}",
        "X-Bonita-API-Token": tokens['X-Bonita-API-Token'],
        "Content-Type": "application/json"
    }
    return headers

def carga_material_recolectado(request):
    headers = get_bonita_tokens(request) # Obtiene los tokens de la sesión, deberiamos cambiar las credenciales del centro para que coincidan con las de algun usuario de bonita
    username = request.session['user']['email'].split('@')[0]

    if headers:
        # Le pego a la API de Bonita que busca el ID del proceso
        url = "http://localhost:8080/bonita/API/bpm/process?f=name=Proceso%20de%20recolecci%C3%B3n&p=0&c=10" 
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:

            # Antes de instanciar el proceso tengo que saber si no hay una instancia ya hecha para esa recolección:
            if (request.session.get('case_id')):
                case_id = request.session['case_id']

                # Obtengo el id de la tarea
                url = f"http://localhost:8080/bonita/API/bpm/task?p=0&c=10&f=caseId={case_id}" 
                response = requests.get(url, headers=headers)
                task_id = response.json()[0]['id']
            else:
                # Obtengo el id del proceso
                process_id = response.json()[0]['id']

                # Le pego a la API de Bonita que instancia el proceso
                url = f"http://localhost:8080/bonita/API/bpm/process/{process_id}/instantiation" 
                response = requests.post(url, headers=headers)
                request.session['case_id'] = response.json()['caseId']
                case_id = response.json()['caseId']

                # Le pego a la API de Bonita que obtiene la tarea (task)
                url = f"http://localhost:8080/bonita/API/bpm/task?p=0&c=10&f=caseId={case_id}" 
                response = requests.get(url, headers=headers)
                task_id = response.json()[0]['id'] # Este es el id de la tarea/task

                # Le pego a la API de Bonita que obtiene el usuario
                url = f"http://localhost:8080/bonita/API/identity/user?p=0&c=10&f=userName={username}" 
                response_user = requests.get(url, headers=headers)
                
                user_id = response_user.json()[0]['id']
                value = {
                    "assigned_id": f"{user_id}", 
                    "state": "ready",
                    #"assign": "true"
                }
                
                # Le pego a la API de Bonita que le asigna la task al usuario
                url = f"http://localhost:8080/bonita/API/bpm/userTask/{task_id}" 
                requests.put(url, headers=headers, data=json.dumps(value))
                
            
            ok = request.POST.get('finalize_task')
            ok_value = {"type": "java.lang.String", "value": "verdadero" if ok else "falso"} 
            # Le pego a la API de Bonita que setea la variable de instancia del 
            # proceso (setea la variable del case)
            url = f"http://localhost:8080/bonita/API/bpm/caseVariable/{case_id}/ok" 
            requests.put(url, headers=headers, data=json.dumps(ok_value))

            if ok:
                # Le pego a la API de Bonita que finaliza la tarea
                url = f"http://localhost:8080/bonita/API/bpm/userTask/{task_id}/execution?assign=true"
                requests.post(url, headers=headers)

                # Almaceno el case_id en la BD
                if request.POST.get("id_recoleccion"):
                    recoleccion = Recoleccion.objects.get(id=request.POST.get("id_recoleccion"))
                else:
                    recoleccion = Recoleccion.objects.get(id=request.session["id_recoleccion"])
                recoleccion.case_id = case_id
                recoleccion.save()
            

            return JsonResponse(response.json(), safe=False)
        else:
            print(f"Error al obtener procesos: {response.status_code}")
            return JsonResponse({"error": "No se pudo autenticar con Bonita"}, status=400)
    else:
        print("No se pudo autenticar con Bonita")
        return JsonResponse({"error": "No se pudo autenticar con Bonita"}, status=400)

def consolidacion_materiales_entregados(request):
    headers = get_bonita_tokens(request)
    username = request.session['user']['email'].split('@')[0]

    if headers:
        # Obtengo el id de la tarea
        recoleccion_id = request.POST.get('id_recoleccion')
        id_case = int(Recoleccion.objects.get(id=recoleccion_id).case_id) 
        url = f"http://localhost:8080/bonita/API/bpm/task?p=0&c=10&f=caseId={id_case}" 
        response = requests.get(url, headers=headers)
        task_id = response.json()[0]['id']
        
        # Le pego a la API de Bonita que obtiene el usuario
        url = f"http://localhost:8080/bonita/API/identity/user?p=0&c=10&f=userName={username}" 
        response_user = requests.get(url, headers=headers)
        
        user_id = response_user.json()[0]['id']
        value = {
            "assigned_id": f"{user_id}", 
            "state": "ready",
            #"assign": "true"
        }
        
        # Le pego a la API de Bonita que le asigna la task al usuario
        url = f"http://localhost:8080/bonita/API/bpm/userTask/{task_id}" 
        requests.put(url, headers=headers, data=json.dumps(value))

        url = f"http://localhost:8080/bonita/API/bpm/userTask/{task_id}/execution?assign=true"
        requests.post(url, headers=headers)
    else:
        raise Exception("No se pudo autenticar con Bonita")
    
def iniciar_sesion_dep(request):
    headers = get_bonita_tokens(request) 
    username = request.data.get("email").split('@')[0]

    if headers:
        # Le pego a la API de Bonita que busca el ID del proceso
        url = "http://localhost:8080/bonita/API/bpm/process?f=name=Proceso%20de%20distribucion%20de%20materiales&p=0&c=10" 
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Obtengo el id del proceso
            process_id = response.json()[0]['id']

            # Le pego a la API de Bonita que instancia el proceso
            url = f"http://localhost:8080/bonita/API/bpm/process/{process_id}/instantiation" 
            response = requests.post(url, headers=headers)
            #request.session['case_id'] = response.json()['caseId']
            case_id = response.json()['caseId']

            # Le pego a la API de Bonita que obtiene la tarea (task)
            url = f"http://localhost:8080/bonita/API/bpm/task?p=0&c=10&f=caseId={case_id}" 
            response = requests.get(url, headers=headers)
            task_id = response.json()[0]['id'] # Este es el id de la tarea/task
            # Le pego a la API de Bonita que obtiene el usuario
            url = f"http://localhost:8080/bonita/API/identity/user?p=0&c=10&f=userName={username}" 
            response_user = requests.get(url, headers=headers)
            
            user_id = response_user.json()[0]['id']
            value = {
                "assigned_id": f"{user_id}", 
                "state": "ready",
                #"assign": "true"
            }
            
            # Le pego a la API de Bonita que le asigna la task al usuario
            url = f"http://localhost:8080/bonita/API/bpm/userTask/{task_id}" 
            requests.put(url, headers=headers, data=json.dumps(value))
            url = f"http://localhost:8080/bonita/API/bpm/userTask/{task_id}/execution?assign=true"
            requests.post(url, headers=headers)

            return case_id
        
def fin_distribucion(request, ok):
    headers = get_bonita_tokens(request) 
    username = request.data.get("email").split('@')[0]

    if headers:
        case_id = request.headers.get('X-Case-ID')

        # Le pego a la API de Bonita que obtiene la tarea (task)
        url = f"http://localhost:8080/bonita/API/bpm/task?p=0&c=10&f=caseId={case_id}" 
        response = requests.get(url, headers=headers)
        task_id = response.json()[0]['id'] # Este es el id de la tarea/task
        # Le pego a la API de Bonita que obtiene el usuario
        url = f"http://localhost:8080/bonita/API/identity/user?p=0&c=10&f=userName={username}" 
        response_user = requests.get(url, headers=headers)
        
        user_id = response_user.json()[0]['id']
        value = {
            "assigned_id": f"{user_id}", 
            "state": "ready",
            #"assign": "true"
        }
        
        # Le pego a la API de Bonita que le asigna la task al usuario
        url = f"http://localhost:8080/bonita/API/bpm/userTask/{task_id}" 
        requests.put(url, headers=headers, data=json.dumps(value))

        ok_value = {"type": "java.lang.String", "value": "verdadero" if ok else "falso"} 
        url = f"http://localhost:8080/bonita/API/bpm/caseVariable/{case_id}/ok" 
        requests.put(url, headers=headers, data=json.dumps(ok_value))

        url = f"http://localhost:8080/bonita/API/bpm/userTask/{task_id}/execution?assign=true"
        requests.post(url, headers=headers)
