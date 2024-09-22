from rest_framework import viewsets
from .models import Estudiantes, Materias
from .serializer import EstudiantesSerializer
from django.shortcuts import render
import urllib.request
import json
from django.http import HttpResponse
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
        url = f'http://127.0.0.1:8000/horario/estudiantesJSON/{id_estudiante}/?format=json'
        with urllib.request.urlopen(url) as response:
            data = json.load(response)

        estudiante_nombre = data.get('nombre', 'Desconocido')
        horario = data.get('horario', [])

        horario_diccionario = {inicio: {
            "hora_inicio": inicio,
            "hora_fin": fin,
            **{dia: "" for dia in dias_semana}
        } for inicio, fin in intervalos}

        for clase in horario:
            dia = clase.get('dia_semana', '')
            materia_nombre = clase.get('nombre_materia', 'Materia Desconocida')  
            profesor = clase.get('profesor', '')
            aula = clase.get('salon', 'Aula X')
            hora_inicio = clase.get('hora_inicio', '')
            hora_fin = clase.get('hora_fin', '')

            for inicio, fin in intervalos:
                if hora_inicio <= inicio and hora_fin > inicio:  
                    if horario_diccionario[inicio][dia] == "":
                        horario_diccionario[inicio][dia] = f"{materia_nombre}<br>{profesor} - {aula}"
                    else:
                        horario_diccionario[inicio][dia] += f"<br>{materia_nombre}<br>{profesor} - {aula}"

        horario_lista = sorted(horario_diccionario.values(), key=lambda x: x['hora_inicio'])

        context = {
            "estudiante": {"nombre": estudiante_nombre},
            "horario_lista": horario_lista
        }

        return render(request, 'horario_estudiante.html', context)

    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)