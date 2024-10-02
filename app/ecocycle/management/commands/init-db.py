import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from ecocycle.models.managers.user import CustomUser
from ecocycle.models.recolector import Recolector
from ecocycle.models.punto import Punto
from ecocycle.models.centro import Centro
from ecocycle.models.material import Material
from ecocycle.models.recoleccion_material import RecoleccionMaterial

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
        CustomUser.objects.all().delete()
        Recolector.objects.all().delete()
        Punto.objects.all().delete()
        Material.objects.all().delete()
        RecoleccionMaterial.objects.all().delete()

    def create_example_data(self):
        # Superusuario
        CustomUser.objects.create_superuser(email='admin@ecocycle.com', password='admin123')

        # Recolectores
        r1 = Recolector.objects.create(nombre='John', apellido='Doe', email='johndoe@example.com', password='123')
        Recolector.objects.create(nombre='Miguel', apellido='Borja', email='dios@gmail.com', password='123')
        Recolector.objects.create(nombre='Marcelo', apellido='Gallardo', email='sapardo@gmail.com', password='123')

        # Bonitos
        r2 = Recolector.objects.create(nombre='Walter', apellido='Bates', email='walter.bates@example.com', password='bpm')
        r3 = Recolector.objects.create(nombre='Jan', apellido='Fisher', email='jan.fisher@example.com', password='bpm')
        r4 = Recolector.objects.create(nombre='William', apellido='Jobs', email='william.jobs@example.com', password='bpm')

        # Puntos de recoleccion
        p1 = Punto.objects.create(nombre='Taller mecanico Carlitos', direccion='Calle 1 1230', password='123', email='punto1@example.com')
        p2 = Punto.objects.create(nombre='Punto 2', direccion='Calle 2', password='123', email='punto2@example.com')

        # Centros de acopio
        Centro.objects.create(nombre='Centro de acopio La Plata', direccion='Av. 7 1850', password='123', email='centro1@example.com')

        # Materiales
        m1 = Material.objects.create(nombre='Aluminio', precio=0.5)
        m2 = Material.objects.create(nombre='Acero', precio=0.3)
        m3 = Material.objects.create(nombre='Carton', precio=0.1)
        m4 = Material.objects.create(nombre='Vidrio', precio=0.2)
        m4 = Material.objects.create(nombre='Plástico', precio=0.3)

        # Recolecciones
        rc1 = r1.recolecciones.create(
            semana=datetime.date(2024, 10, 7),
            pago=sum([m1.precio, m2.precio, m3.precio]),
            observaciones='Ninguna'
        )
        RecoleccionMaterial.objects.create(recoleccion=rc1, material=m1, cantidad=1)
        RecoleccionMaterial.objects.create(recoleccion=rc1, material=m2, cantidad=2)
        RecoleccionMaterial.objects.create(recoleccion=rc1, material=m3, cantidad=3)

        # Asignacion de Puntos a Recolectores
        r1.puntos.add(p1)
        r2.puntos.add(p1)
        r3.puntos.add(p2)
        r4.puntos.add(p2)
