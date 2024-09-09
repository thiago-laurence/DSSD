from django.contrib import admin

from ecocycle.models.recolector import Recolector
from ecocycle.models.administrador import Administrador
from ecocycle.models.deposito import Deposito
from ecocycle.models.punto import Punto
from ecocycle.models.centro import Centro

admin.site.register(Recolector)
admin.site.register(Administrador)
admin.site.register(Deposito)
admin.site.register(Punto)
admin.site.register(Centro)