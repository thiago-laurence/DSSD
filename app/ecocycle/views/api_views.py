import requests
from django.http import JsonResponse
from django.shortcuts import render

def index(request):
    obj = obtener_procesos(request)
    return render(request, 'api/index.html', {'procesos': obj})

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
        x_bonita_api_token = response.headers.get('X-Bonita-API-Token')

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
            "Cookie": f"JSESSIONID={tokens['jsessionid']}",
            "X-Bonita-API-Token": tokens['api-token']
        }
        url = "http://localhost:8080/bonita/API/bpm/process?p=0&c=10"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener procesos: {response.status_code}")
            return None
    else:
        print("No se pudo autenticar con Bonita")
        return None
