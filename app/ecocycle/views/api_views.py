import json
from django.http import JsonResponse
import requests
from django.shortcuts import render
from os import environ as env

def index(request):
    obj = obtener_procesos(request)
    return render(request, 'api/index.html', {'obj': obj})

def login_bonita(request):
    url = "http://localhost:8080/bonita/loginservice"
    username = request.session['user']['email'].split('@')[0]
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
        print(f"Error al autenticar: {response.status_code}")
        return None

def get_bonita_tokens(request):
    tokens = request.session.get('bonita_tokens')
    if not tokens:
        tokens = login_bonita(request)
    return tokens

def obtener_procesos(request):
    tokens = get_bonita_tokens(request)
    username = request.session['user']['email'].split('@')[0]
    material_tipo = request.POST.get("material_tipo")
    material_cantidad = request.POST.get("material_cantidad")

    if tokens:
        headers = {
            "Cookie": f"JSESSIONID={tokens['JSESSIONID']}",
            "X-Bonita-API-Token": tokens['X-Bonita-API-Token'],
            "Content-Type": "application/json"
        }
        # Le pego a la API de Bonita que busca el ID del proceso
        url = "http://localhost:8080/bonita/API/bpm/process?f=name=Proceso%20de%20recolecci%C3%B3n&p=0&c=10" 
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Obtengo el id del proceso
            process_id = response.json()[0]['id']

            # Antes de instanciar el proceso tengo que saber si no hay una instancia ya hecha para esa recolección:
            if (request.session.get('recoleccion_id')):
                case_id = request.session['recoleccion_id']
            else:
                # Le pego a la API de Bonita que instancia el proceso
                url = f"http://localhost:8080/bonita/API/bpm/process/{process_id}/instantiation" 
                response = requests.post(url, headers=headers)
                request.session['recoleccion_id'] = response.json()['caseId']
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
                response = requests.put(url, headers=headers, data=json.dumps(value))
            
            ok = request.POST.get('finalize_process')
            ok_value = {"type": "java.lang.String", "value": "verdadero" if ok else "falso"} 
            # Le pego a la API de Bonita que setea la variable de instancia del 
            # proceso (setea la variable del case)
            url = f"http://localhost:8080/bonita/API/bpm/caseVariable/{case_id}/ok" 
            response = requests.put(url, headers=headers, data=json.dumps(ok_value))

            if ok:
                # Le pego a la API de Bonita que finaliza la tarea
                url = f"http://localhost:8080/bonita/API/bpm/userTask/{task_id}/execution?assign=true"
                requests.post(url, headers=headers)
            
            return JsonResponse(response.json(), safe=False)
        else:
            print(f"Error al obtener procesos: {response.status_code}")
            return JsonResponse({"error": "No se pudo autenticar con Bonita"}, status=400)
    else:
        print("No se pudo autenticar con Bonita")
        return JsonResponse({"error": "No se pudo autenticar con Bonita"}, status=400)



            #Setea las variables del material
            #material_tipo_value = {"type": "java.lang.String", "value": material_tipo} 
            #url = f"http://localhost:8080/bonita/API/bpm/caseVariable/{case_id}/material_tipo"
            #response = requests.put(url, headers=headers, data=json.dumps(material_tipo_value))

            #Setea las variables de la cantidad
            #material_cantidado_value = {"type": "java.lang.String", "value": material_cantidad} 
            #url = f"http://localhost:8080/bonita/API/bpm/caseVariable/{case_id}/material_cantidad" 
            #response = requests.put(url, headers=headers, data=json.dumps(material_cantidado_value))
