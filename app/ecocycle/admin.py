from django.contrib import admin

from ecocycle.models.recolector import Recolector
from ecocycle.models.administrador import Administrador
from ecocycle.models.deposito import Deposito
from ecocycle.models.punto import Punto
from ecocycle.models.centro import Centro
from ecocycle.models.material import Material
from ecocycle.models.recoleccion import Recoleccion
from ecocycle.models.recoleccion_material import RecoleccionMaterial
from ecocycle.models.centro_material import CentroMaterial

admin.site.register(Recolector)
admin.site.register(Administrador)
admin.site.register(Deposito)
admin.site.register(Punto)
admin.site.register(Centro)
admin.site.register(Material)
admin.site.register(Recoleccion)
admin.site.register(RecoleccionMaterial)
admin.site.register(CentroMaterial)