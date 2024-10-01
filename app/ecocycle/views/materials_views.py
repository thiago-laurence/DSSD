from django.shortcuts import render, redirect
from . import api_views
from ..forms import RecoleccionForm

def index(request):
    return render(request, 'materials/index.html')

def send(request):
    api_views.obtener_procesos(request)
    if request.POST.get('finalize_process') != 'on':
        return render(request, 'materials/index.html')
    else:
        return redirect('/')
    