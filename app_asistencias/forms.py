from django import forms
from .models import Asistencia
from app_horario.models import CodigosHora

class AsistenciaForm(forms.ModelForm):
    codigo_hora = forms.ModelChoiceField(
        queryset=CodigosHora.objects.all(),
        label="Materia Info",
        widget=forms.Select,
        to_field_name='id',
    )

    class Meta:
        model = Asistencia
        fields = '__all__'
        labels = {
            'codigo_hora': 'Materia Info',
        }

    def __init__(self, *args, **kwargs):
        super(AsistenciaForm, self).__init__(*args, **kwargs)
        # Personaliza las opciones del campo para que muestren más detalles
        self.fields['codigo_hora'].label_from_instance = lambda obj: f"{obj.id_materia.nombre_materia} - {obj.dia_semana} - {obj.salon} - {obj.hora_inicio} a {obj.hora_fin}"
