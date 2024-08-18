from django.contrib import admin
from .models import Estudiantes, Facultades, Carreras, Materias, CodigosHora, Matriculas, MateriasCarreras

@admin.register(Estudiantes)
class EstudiantesAdmin(admin.ModelAdmin):
    list_display = ('id_estudiante', 'nombre')

@admin.register(Facultades)
class FacultadesAdmin(admin.ModelAdmin):
    list_display = ('id_facultad', 'nombre_facultad')

@admin.register(Carreras)
class CarrerasAdmin(admin.ModelAdmin):
    list_display = ('id_carrera', 'nombre_carrera', 'id_facultad')

@admin.register(Materias)
class MateriasAdmin(admin.ModelAdmin):
    list_display = ('id_materia', 'nombre_materia')

@admin.register(CodigosHora)
class CodigosHoraAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo_hora', 'id_materia', 'id_carrera', 'id_facultad', 'dia_semana', 'hora_inicio', 'hora_fin', 'salon', 'profesor')

@admin.register(Matriculas)
class MatriculasAdmin(admin.ModelAdmin):
    list_display = ('id_estudiante', 'id_codigo')

@admin.register(MateriasCarreras)
class MateriasCarrerasAdmin(admin.ModelAdmin):
    list_display = ('id_materia', 'id_carrera')
