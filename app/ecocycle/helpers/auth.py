from ecocycle.models.recolector import Recolector
from ecocycle.models.centro import Centro

def do_downcasting(user):
    match user.subclase:
        case 'recolector':
            return Recolector.objects.get(pk=user.id)
        case 'centro':
            return Centro.objects.get(pk=user.id)