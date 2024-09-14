from rest_framework import viewsets
from .models import Estudiantes, Matriculas, CodigosHora
from .serializer import EstudiantesSerializer
from django.shortcuts import render
from datetime import datetime, time, timedelta

class EstudiantesViewSet(viewsets.ModelViewSet):
    queryset = Estudiantes.objects.all()
    serializer_class = EstudiantesSerializer

# Definir los intervalos de tiempo exactos
intervalos = [
    ("07:50:00", "08:35:00"),
    ("08:40:00", "09:25:00"),
    ("09:30:00", "10:15:00"),
    ("10:20:00", "11:05:00"),
    ("11:10:00", "11:55:00"),
    ("12:00:00", "12:45:00"),
    ("12:50:00", "13:35:00")
]

dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

def estudiante_detalle(request, id_estudiante):
    try:
        estudiante = Estudiantes.objects.get(id_estudiante=id_estudiante)
        matriculas = Matriculas.objects.filter(id_estudiante=estudiante)

        # Inicializar un diccionario para organizar el horario por intervalo
        horario_diccionario = {inicio: {
            "hora_inicio": inicio,
            "hora_fin": fin,
            **{dia: "" for dia in dias_semana}
        } for inicio, fin in intervalos}

        for matricula in matriculas:
            codigo_hora = matricula.id_codigo
            dia = codigo_hora.dia_semana
            materia = codigo_hora.id_materia.nombre_materia
            profesor = codigo_hora.profesor
            salon = codigo_hora.salon  # Asegúrate de que 'aula' esté disponible
            hora_inicio = codigo_hora.hora_inicio.strftime("%H:%M:%S")
            hora_fin = codigo_hora.hora_fin.strftime("%H:%M:%S")

            for inicio, fin in intervalos:
                if hora_inicio <= inicio and hora_fin > inicio:
                    contenido = f"{materia}<br>{profesor} - Aula {salon}"
                    if horario_diccionario[inicio][dia] == "":
                        horario_diccionario[inicio][dia] = contenido
                    else:
                        horario_diccionario[inicio][dia] += f"<br>{contenido}"

        # Convertir el diccionario a una lista para pasar a la plantilla
        horario_lista = sorted(horario_diccionario.values(), key=lambda x: x['hora_inicio'])

        context = {
            "estudiante": estudiante,
            "horario_lista": horario_lista
        }

        return render(request, 'horario_estudiante.html', context)

    except Estudiantes.DoesNotExist:
        return render(request, '404.html', {"error": "Estudiante no encontrado"}, status=404)