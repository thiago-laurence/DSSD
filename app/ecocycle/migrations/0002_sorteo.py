# Generated by Django 5.1 on 2024-11-17 21:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecocycle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sorteo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('numero', models.IntegerField(unique=True)),
                ('deposito', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sorteos', to='ecocycle.deposito')),
            ],
            options={
                'db_table': 'sorteo',
            },
        ),
    ]
