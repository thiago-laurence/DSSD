# Generated by Django 5.1 on 2024-11-02 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecocycle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recoleccion',
            name='case_id',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
