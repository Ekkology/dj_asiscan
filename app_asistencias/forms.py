from django import forms
from .models import Asistencia

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = '__all__'  # Incluye todos los campos del modelo
        widgets = {
            'codigo_hora': forms.Select(attrs={'placeholder': 'Materia Info'}),  # Cambio visual del campo
        }
        labels = {
            'codigo_hora': 'Materia Info',  # Cambia el nombre del campo en el formulario
        }
