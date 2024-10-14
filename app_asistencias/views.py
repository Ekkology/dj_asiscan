from rest_framework import viewsets
from .models import Asistencia
from .serializer import AsistenciaSerializer
from django.http import JsonResponse
import json
from datetime import datetime
from django.utils.timezone import now
from app_horario.models import Estudiantes, CodigosHora
from django.views.decorators.csrf import csrf_exempt

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

@csrf_exempt
def registrar_asistencia(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        nombres = data.get('nombres', [])
        dia_simulado = data.get('dia_simulado', now().strftime("%A"))
        hora_simulada = data.get('hora_simulada', now().strftime("%H:%M:%S"))
        estudiantes = Estudiantes.objects.filter(nombre__in=nombres)

        asistencia_registrada = []
        asistencia_duplicada = []

        for estudiante in estudiantes:
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
            "asistencia_registrada": asistencia_registrada
        }

        if asistencia_duplicada:
            response_data["asistencia_duplicada"] = asistencia_duplicada

        return JsonResponse(response_data)

    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)
