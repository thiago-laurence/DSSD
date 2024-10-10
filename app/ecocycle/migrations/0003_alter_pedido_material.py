# Generated by Django 5.1.1 on 2024-10-10 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecocycle', '0002_pedido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='material',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='ecocycle.material'),
        ),
    ]
