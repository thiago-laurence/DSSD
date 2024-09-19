from django.shortcuts import redirect, render
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from ecocycle.models.recolector import Recolector

@api_view(['GET'])
def index(request):
    if 'user' in request.session:
        return redirect('recolector:index')
    
    return render(request, 'login/index.html')

@api_view(['POST'])
def auth(request):
    username = request.data.get('email')
    password = request.data.get('password')

    user = Recolector.objects.filter(email=username).first()

    if (user is None) or (not check_password(password, user.password)):
        return render(request, 'login/index.html', {'failed': True})

    request.session['user'] = {
        'id': user.id,
        'name': user.nombre + ' ' + user.apellido,
        'email': user.email,
        'puntos': list(user.puntos.values('id', 'nombre', 'direccion')),
    }

    return redirect('recolector:index')

@api_view(['GET'])
def logout(request):
    request.session.flush()

    return redirect('login:index')