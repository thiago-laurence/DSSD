from ecocycle.models.recolector import Recolector
from ecocycle.models.punto import Punto

def do_downcasting(user):
    match user.subclase:
        case 'recolector':
            return Recolector.objects.get(pk=user.id)
        case 'punto':
            return Punto.objects.get(pk=user.id)