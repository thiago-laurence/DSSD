# Generated by Django 5.1.1 on 2024-10-16 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecocycle', '0003_punto_materiales'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedido',
            old_name='fecha',
            new_name='fecha_creacion',
        ),
        migrations.AddField(
            model_name='pedido',
            name='fecha_envio',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='fecha_reserva',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='fecha_solicitada',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
