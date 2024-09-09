from django.db import models
from .usuario import Usuario

class Recolector(Usuario):
    puntos = models.ManyToManyField('Punto', related_name='recolectores', blank=True)