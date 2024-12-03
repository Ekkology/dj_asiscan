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
import logging


class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

def procesar_nombre(name_person):
    """Procesa un nombre en formato 'apellido-nombre' para normalizarlo."""
    partes = name_person.split('-')
    return ' '.join(p.capitalize() for p in reversed(partes))

logger = logging.getLogger(__name__)

@csrf_exempt
def registrar_asistencia(request):
    if request.method == 'GET':
        api_url = "http://asiscan.sytes.net/cam/api/face-recognition2"
        try:
            with urllib.request.urlopen(api_url) as response:
                data = json.loads(response.read().decode())
        except urllib.error.URLError as e:
            return JsonResponse({"status": "error", "message": f"Error al obtener datos: {str(e)}"}, status=500)

        personas_verificadas = data.get('verified', [])
        fecha_actual = datetime.now().date()
        hora_actual = datetime.now().time()
        dia_actual_ingles = datetime.now().strftime("%A")

        # Diccionario para traducir días en inglés a español
        dias_traduccion = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }

        # Obtener el día en español
        dia_actual = dias_traduccion.get(dia_actual_ingles, dia_actual_ingles)

        # Log de la fecha, hora y día actual
        print(f"Fecha actual: {fecha_actual}, Hora actual: {hora_actual}, Día actual: {dia_actual}")

        # Cargar estudiantes de la base de datos
        nombres_estudiantes = {e.nombre: e for e in Estudiantes.objects.all()}

        asistencia_registrada = []
        asistencia_duplicada = []
        no_encontrados = []

        for persona in personas_verificadas:
            name_person = persona.get('name_person')
            if not name_person:
                continue

            # Log: Nombre en 'name_person' encontrado
            print(f"Nombre en 'name_person' encontrado: {name_person}")

            # Procesar el nombre
            nombre_procesado = procesar_nombre(name_person)

            # Log: Nombre procesado final
            print(f"Nombre procesado: {nombre_procesado}")

            # Buscar coincidencias en la base de datos de estudiantes
            coincidencias = get_close_matches(nombre_procesado, nombres_estudiantes.keys(), n=1, cutoff=0.5)

            if not coincidencias:
                no_encontrados.append(name_person)
                print(f"No se encontraron coincidencias para: {name_person}")
                continue

            # Log: Coincidencia encontrada
            nombre_estudiante = coincidencias[0]
            estudiante = nombres_estudiantes[nombre_estudiante]
            print(f"Coincidencia encontrada: {estudiante.nombre}")

            # Buscar materias correspondientes al día y hora actuales
            materias = CodigosHora.objects.filter(
                dia_semana=dia_actual,
                hora_inicio__lte=hora_actual,
                hora_fin__gt=hora_actual
            )

            if materias.exists():
                print(f"Materia encontrada para la hora actual: {materias.first().codigo_hora}")
            else:
                # Si no hay materias para la hora actual, buscar la última materia del día
                materias = CodigosHora.objects.filter(
                    dia_semana=dia_actual
                ).order_by('-hora_fin')[:1]
                if materias.exists():
                    print(f"No se encontró materia para la hora actual, se usará la última materia del día: {materias.first().codigo_hora}")
                else:
                    # Si no hay materias en todo el día
                    print(f"No hay materias disponibles para el día {dia_actual}")

            # Asegúrate de que 'materias' no esté vacío antes de continuar
            if materias.exists():
                materia = materias.first()

                # Log: Información de la materia encontrada
                print(f"Materia seleccionada: {materia.codigo_hora} - {materia.id_materia.nombre_materia}")

                # Verificar si ya existe una asistencia para esta materia
                existe_asistencia = Asistencia.objects.filter(
                    estudiante=estudiante,
                    codigo_hora=materia,
                    fecha_asistencia=fecha_actual
                ).exists()

                if not existe_asistencia:
                    # Registrar asistencia
                    Asistencia.objects.create(
                        estudiante=estudiante,
                        codigo_hora=materia,
                        fecha_asistencia=fecha_actual,
                        hora_asistencia=hora_actual,
                        asistio=True
                    )
                    asistencia_registrada.append(estudiante.nombre)
                    print(f"Asistencia registrada para {estudiante.nombre} en {materia.codigo_hora} a las {hora_actual}")
                else:
                    asistencia_duplicada.append(estudiante.nombre)
                    print(f"Ya existe una asistencia registrada para {estudiante.nombre} en {materia.codigo_hora}")

            else:
                # Log si no hay materias para registrar asistencia
                print(f"No se encontró ninguna materia para registrar asistencia para {estudiante.nombre}")

        response_data = {
            "status": "success",
            "asistencia_registrada": asistencia_registrada,
            "no_encontrados": no_encontrados,
        }

        if asistencia_duplicada:
            response_data["asistencia_duplicada"] = asistencia_duplicada

        return JsonResponse(response_data)

    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)
