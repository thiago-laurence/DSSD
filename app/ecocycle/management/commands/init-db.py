from django.core.management.base import BaseCommand
from django.db import transaction
from ecocycle.models.recolector import Recolector
from ecocycle.models.punto import Punto

class Command(BaseCommand):
    help = 'Initializes the database with initial datasets'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                self.stdout.write(self.style.WARNING('Eliminando base de datos...'))

                # 1. Eliminar datos existentes
                self.reset_database()

                # 2. Inicializando de datos
                self.stdout.write(self.style.WARNING('Creando datos...'))
                self.create_example_data()

                self.stdout.write(self.style.SUCCESS('Base de datos creada e inicializada con exito!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error durante el proceso: {e}'))

    def reset_database(self):
        Recolector.objects.all().delete()
        Punto.objects.all().delete()

    def create_example_data(self):
        # Recolectores
        r1 = Recolector.objects.create(nombre='John', apellido='Doe', email='johndoe@example.com', password='123')
        # Bonitos
        r2 = Recolector.objects.create(nombre='Walter', apellido='Bates', email='walter.bates@example.com', password='123')
        r3 = Recolector.objects.create(nombre='Jan', apellido='Fisher', email='jan.fisher@example.com', password='123')
        r4 = Recolector.objects.create(nombre='William', apellido='Jobs', email='william.jobs@example.com', password='123')

        # Puntos
        p1 = Punto.objects.create(nombre='Punto 1', direccion='Calle 1', password='123', email='punto1@example.com')
        p2 = Punto.objects.create(nombre='Punto 2', direccion='Calle 2', password='123', email='punto2@example.com')

        # Asignacion de Puntos a Recolectores
        r1.puntos.add(p1)
        r2.puntos.add(p1)
        r3.puntos.add(p2)
        r4.puntos.add(p2)
