from django.shortcuts import redirect, render
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from ecocycle.models.managers.user import CustomUser
from ecocycle.helpers import auth as auth_helper

@api_view(['GET'])
def index(request):
    if 'user' in request.session:
        return redirect(f'{request.session['user']['subclase']}:index')
    
    return render(request, 'login/index.html')

@api_view(['POST'])
def auth(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = CustomUser.objects.filter(email=email).first()

    if (user is None) or (not check_password(password, user.password)):
        return render(request, 'login/index.html', {'failed': True})
    
    user = auth_helper.do_downcasting(user)
    request.session['user'] = user.to_dict()

    return redirect(f'{user.subclase}:index')

@api_view(['GET'])
def logout(request):
    request.session.flush()

    return redirect('login:index')