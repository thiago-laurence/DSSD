from django import forms
#from .models import Recoleccion

class RecoleccionForm(forms.ModelForm):
    class Meta:
        #model = Recoleccion
        fields = ['id', 'id_recolector', 'id_local', 'semana', 'pago', 'observaciones']
        