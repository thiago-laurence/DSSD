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
        url = "http://localhost:8080/bonita/API/bpm/process?f=name=Proceso%20de%20recolecci%C3%B3n&p=0&c=10" # Le pego a la API de Bonita que busca el ID del proceso
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            process_id = response.json()[0]['id'] # Obtengo el id del proceso
            url = f"http://localhost:8080/bonita/API/bpm/process/{process_id}/instantiation" # Le pego a la API de Bonita que instancia el proceso
            response = requests.post(url, headers=headers)
            
            task_id = response.json()['caseId'] # Este es el id de la instancia del proceso 
            
            ok = True
            ok_value = {"type": "java.lang.String", "value": "Verdadero"} 
            url = f"http://localhost:8080/bonita/API/bpm/caseVariable/{task_id}/ok" # Le pego a la API de Bonita que setea la variable de la tarea
            response = requests.put(url, headers=headers, data=json.dumps(ok_value))


            url = f"http://localhost:8080/bonita/API/bpm/task?p=0&c=10&f=caseId={task_id}" # Le pego a la API de Bonita que obtiene la tarea
            response = requests.get(url, headers=headers)
            task_id = response.json()[0]['id'] # Este es el id de la tarea (creo)
            
            url = f"http://localhost:8080/bonita/API/identity/user?p=0&c=10&f=userName=walter.bates" # Le pego a la API de Bonita que obtiene el usuario
            response_user = requests.get(url, headers=headers)

            value = {
                "assigned_id": f"{response_user.json()[0]['id']}",
                "state": "new_state"}
            url = f"http://localhost:8080/bonita/API/bpm/humanTask/{response_user.json()[0]['id']}" # Le pego a la API de Bonita que ejecuta la tarea
            response = requests.put(url, headers=headers, data=json.dumps(value))

            

            url = f"http://localhost:8080/bonita/API/bpm/userTask/{task_id}/execution"
            response = requests.post(url, headers=headers)

            # return response.json()
        else:
            print(f"Error al obtener procesos: {response.status_code}")
            return None
    else:
        print("No se pudo autenticar con Bonita")
        return None
