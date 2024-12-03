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
    


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Estudiantes, Matriculas
from .serializer import CodigosHoraSerializer

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Buscar el estudiante asociado al usuario
            try:
                estudiante = Estudiantes.objects.get(user=user)
                return redirect('horario_estudiante', id_estudiante=estudiante.id_estudiante)
            except Estudiantes.DoesNotExist:
                return render(request, 'login.html', {'error': 'No se encontr� estudiante asociado'})
        else:
            return render(request, 'login.html', {'error': 'Credenciales inv�lidas'})
    return render(request, 'login.html')


from app_asistencias.models import Asistencia
from django.utils import timezone


@login_required
def horario_estudiante(request, id_estudiante):
    try:
        estudiante = Estudiantes.objects.get(id_estudiante=id_estudiante)
        
        # Obtener las asistencias del estudiante para la semana actual
        today = timezone.now().date()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        end_of_week = start_of_week + timezone.timedelta(days=6)
        
        asistencias = Asistencia.objects.filter(
            estudiante=estudiante,
            fecha_asistencia__range=[start_of_week, end_of_week],
            asistio=True
        )
        
        # Obtener los c�digos de hora con asistencia
        codigos_hora_asistencia = set(asistencia.codigo_hora_id for asistencia in asistencias)
        
        matriculas = Matriculas.objects.filter(id_estudiante=estudiante)
        horarios = CodigosHoraSerializer([matricula.id_codigo for matricula in matriculas], many=True).data
        
        context = {
            'estudiante': estudiante,
            'horarios': horarios,
            'asistencias_por_clase': codigos_hora_asistencia
        }

        








        
        return render(request, 'horario.html', context)
    except Estudiantes.DoesNotExist:
        return render(request, 'error.html', {'mensaje': 'Estudiante no encontrado'})

