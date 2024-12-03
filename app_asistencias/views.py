from rest_framework import viewsets
from .models import Asistencia
from .serializer import AsistenciaSerializer
from django.http import JsonResponse
import json
from datetime import datetime
from django.utils.timezone import now
from app_horario.models import Estudiantes, CodigosHora
from django.views.decorators.csrf import csrf_exempt
from difflib import get_close_matches
import urllib.request

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

@csrf_exempt
def registrar_asistencia(request):
    if request.method == 'GET':
        api_url = "http://asiscan.sytes.net/api/latest-image/"
        try:
            with urllib.request.urlopen(api_url) as response:
                data = json.loads(response.read().decode())
        except urllib.error.URLError as e:
            return JsonResponse({"status": "error", "message": f"Error al obtener datos: {str(e)}"}, status=500)

        personas_verificadas = data.get('verified', [])
        dia_simulado = now().strftime("%A")
        hora_simulada = now().strftime("%H:%M:%S")

        nombres_estudiantes = {e.nombre: e for e in Estudiantes.objects.all()}

        asistencia_registrada = []
        asistencia_duplicada = []
        no_encontrados = []

        for persona in personas_verificadas:
            name_person = persona.get('name_person')
            if not name_person:
                continue

            coincidencias = get_close_matches(name_person, nombres_estudiantes.keys(), n=1, cutoff=0.5)
            if not coincidencias:
                no_encontrados.append(name_person)
                continue

            nombre_estudiante = coincidencias[0]
            estudiante = nombres_estudiantes[nombre_estudiante]

            materias = CodigosHora.objects.filter(
                dia_semana=dia_simulado,
                hora_inicio__lte=hora_simulada,
                hora_fin__gt=hora_simulada
            )

            for materia in materias:
                existe_asistencia = Asistencia.objects.filter(
                    estudiante=estudiante,
                    codigo_hora=materia,
                    fecha_asistencia=datetime.now().date()
                ).exists()

                if not existe_asistencia:
                    Asistencia.objects.create(
                        estudiante=estudiante,
                        codigo_hora=materia,
                        fecha_asistencia=datetime.now().date(),
                        hora_asistencia=hora_simulada,
                        asistio=True
                    )
                    asistencia_registrada.append(estudiante.nombre)
                else:
                    asistencia_duplicada.append(estudiante.nombre)

                break

        response_data = {
            "status": "success",
            "asistencia_registrada": asistencia_registrada,
            "no_encontrados": no_encontrados,
        }

        if asistencia_duplicada:
            response_data["asistencia_duplicada"] = asistencia_duplicada

        return JsonResponse(response_data)

    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)
