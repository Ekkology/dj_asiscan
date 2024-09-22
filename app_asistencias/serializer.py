from rest_framework import serializers
from .models import Asistencia

class AsistenciaSerializer(serializers.ModelSerializer):
    nombre_estudiante = serializers.CharField(source='estudiante.nombre')
    codigo_hora = serializers.CharField(source='codigo_hora.codigo_hora')
    nombre_materia = serializers.CharField(source='codigo_hora.id_materia.nombre_materia')
    dia_semana = serializers.CharField(source='codigo_hora.dia_semana')
    hora_inicio = serializers.TimeField(source='codigo_hora.hora_inicio')
    hora_fin = serializers.TimeField(source='codigo_hora.hora_fin')
    
    class Meta:
        model = Asistencia
        fields = ['nombre_estudiante', 'codigo_hora', 'nombre_materia', 'dia_semana', 'hora_inicio', 'hora_fin', 'fecha_asistencia', 'hora_asistencia', 'asistio']
