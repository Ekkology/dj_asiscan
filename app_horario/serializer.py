from rest_framework import serializers
from .models import Estudiantes, CodigosHora, Matriculas

class CodigosHoraSerializer(serializers.ModelSerializer):
    nombre_materia = serializers.CharField(source='id_materia.nombre_materia', read_only=True)  

    class Meta:
        model = CodigosHora
        fields = ['codigo_hora', 'id_materia', 'nombre_materia', 'id_carrera', 'id_facultad', 'dia_semana', 'hora_inicio', 'hora_fin', 'salon', 'profesor']

class EstudiantesSerializer(serializers.ModelSerializer):
    horario = serializers.SerializerMethodField()

    class Meta:
        model = Estudiantes
        fields = ['id_estudiante', 'nombre', 'horario']

    def get_horario(self, obj):
        matriculas = Matriculas.objects.filter(id_estudiante=obj)
        return CodigosHoraSerializer([matricula.id_codigo for matricula in matriculas], many=True).data

