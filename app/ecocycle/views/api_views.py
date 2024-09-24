import json
import requests
from django.http import JsonResponse
from django.shortcuts import render

def index(request):
    obj = obtener_procesos(request)
    return render(request, 'api/index.html', {'obj': obj})

def login_bonita(request):
    url = "http://localhost:8080/bonita/loginservice"

    payload = {
        "username": "walter.bates",
        "password": "bpm",
        "redirect": "false"
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
            # Le pego a la API de Bonita que instancia el proceso
            url = f"http://localhost:8080/bonita/API/bpm/process/{process_id}/instantiation" 
            response = requests.post(url, headers=headers)
            print(response)
            
            # Este es el id de la instancia del proceso (un case)
            case_id = response.json()['caseId'] 
            
            ok = request.POST.get('finalize_process')
            ok_value = {"type": "java.lang.String", "value": "verdadero" if ok else "falso"} 
            # Le pego a la API de Bonita que setea la variable de instancia del 
            # proceso (setea la variable del case)
            url = f"http://localhost:8080/bonita/API/bpm/caseVariable/{case_id}/ok" 
            response = requests.put(url, headers=headers, data=json.dumps(ok_value))
            print(response)

            # Le pego a la API de Bonita que obtiene la tarea (task)
            url = f"http://localhost:8080/bonita/API/bpm/task?p=0&c=10&f=caseId={case_id}" 
            response = requests.get(url, headers=headers)
            print(response)
            task_id = response.json()[0]['id'] # Este es el id de la tarea/task (creo)

            # Le pego a la API de Bonita que obtiene el usuario
            url = f"http://localhost:8080/bonita/API/identity/user?p=0&c=10&f=userName=walter.bates" 
            response_user = requests.get(url, headers=headers)
            print("requests.get(url, headers=headers)")
            print(response_user)

            value = {
                # Este es el id del usuario
                "assigned_id": f"{response_user.json()[0]['id']}", 
                "state": "ready"}
            # Le pego a la API de Bonita que le asigna la task al usuario
            url = f"http://localhost:8080/bonita/API/bpm/userTask/{task_id}" 
            response = requests.put(url, headers=headers, data=json.dumps(value))
            print("requests.put(url, headers=headers, data=json.dumps(value))")
            print(response.json())
            
            # Le pego a la API de Bonita que finaliza la tarea
            url = f"http://localhost:8080/bonita/API/bpm/userTask/{task_id}/execution"
            response = requests.post(url, headers=headers)
            print("requests.post(url, headers=headers)")
            print(response.json())

            
            return response.json()
        else:
            print(f"Error al obtener procesos: {response.status_code}")
            return None
    else:
        print("No se pudo autenticar con Bonita")
        return None
