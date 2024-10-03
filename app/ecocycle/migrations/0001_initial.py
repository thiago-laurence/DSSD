# Generated by Django 5.1.1 on 2024-10-03 15:24

import datetime
import django.db.models.deletion
import django.utils.timezone
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('subclase', models.CharField(max_length=50)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'material',
            },
        ),
        migrations.CreateModel(
            name='Recoleccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semana', models.DateField(default=datetime.date.today)),
                ('pago', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('observaciones', models.TextField(default='', max_length=250)),
                ('finalizada', models.BooleanField(default=False)),
                ('notificacion', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'recoleccion',
            },
        ),
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('username', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('ecocycle.customuser',),
        ),
        migrations.CreateModel(
            name='Centro',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('direccion', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('ecocycle.customuser',),
        ),
        migrations.CreateModel(
            name='Deposito',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('direccion', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('ecocycle.customuser',),
        ),
        migrations.CreateModel(
            name='Punto',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('direccion', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('ecocycle.customuser',),
        ),
        migrations.CreateModel(
            name='RecoleccionMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecocycle.material')),
                ('recoleccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecocycle.recoleccion')),
            ],
            options={
                'db_table': 'material_recoleccion',
                'unique_together': {('material', 'recoleccion')},
            },
        ),
        migrations.AddField(
            model_name='recoleccion',
            name='materiales',
            field=models.ManyToManyField(through='ecocycle.RecoleccionMaterial', to='ecocycle.material'),
        ),
        migrations.CreateModel(
            name='CentroMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecocycle.material')),
                ('centro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecocycle.centro')),
            ],
            options={
                'db_table': 'centro_material',
                'unique_together': {('material', 'centro')},
            },
        ),
        migrations.AddField(
            model_name='centro',
            name='materiales',
            field=models.ManyToManyField(through='ecocycle.CentroMaterial', to='ecocycle.material'),
        ),
        migrations.CreateModel(
            name='Recolector',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('username', models.CharField(blank=True, max_length=1000, null=True)),
                ('puntos', models.ManyToManyField(blank=True, related_name='recolectores', to='ecocycle.punto')),
            ],
            options={
                'abstract': False,
            },
            bases=('ecocycle.customuser',),
        ),
        migrations.AddField(
            model_name='recoleccion',
            name='recolector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recolecciones', to='ecocycle.recolector'),
        ),
    ]
