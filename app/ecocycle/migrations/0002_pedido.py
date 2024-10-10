# Generated by Django 5.1 on 2024-10-10 21:10

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecocycle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('centro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ecocycle.centro')),
                ('deposito', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecocycle.deposito')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecocycle.material')),
            ],
            options={
                'db_table': 'pedido',
                'constraints': [models.UniqueConstraint(fields=('deposito', 'material', 'fecha'), name='unique_deposito_material_fecha')],
            },
        ),
    ]
