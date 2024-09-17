from django.db import models

class Material(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'material'

    def __str__(self) -> str:
        return self.nombre