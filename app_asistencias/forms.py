from django import forms
from .models import Asistencia

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['estudiante', 'codigo_hora', 'fecha_asistencia', 'hora_asistencia', 'asistio']
