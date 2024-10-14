from django.shortcuts import redirect
from ecocycle.models.administrador import Administrador
from ecocycle.models.recolector import Recolector
from ecocycle.models.centro import Centro

def do_downcasting(user):
    match user.subclase:
        case 'recolector':
            return Recolector.objects.get(pk=user.id)
        case 'centro':
            return Centro.objects.get(pk=user.id)
        case 'administrador':
            return Administrador.objects.get(pk=user.id)

def login_required(subclase):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if 'user' not in request.session:
                return redirect('login:index')
            
            if request.session['user']['subclase'] != subclase:
                return redirect(f"{request.session['user']['subclase']}:index")
            
            return view(request, *args, **kwargs)
        
        return wrapper
    
    return decorator
