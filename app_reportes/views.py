from django.shortcuts import render

from .serializers import ReporteSerializer
from .models import Asistencia, Reporte #son del otro app
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Estudiante #estan en la otra app
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import Reporte
from rest_framework  import serializers


def generar_reporte_por_estudiante(semestre, estudiante_id):
    # Obtener todas las asistencias del estudiante en un semestre
    asistencias = Asistencia.objects.filter(estudiante_id=estudiante_id, materia__semestre=semestre)

    for asistencia in asistencias:
        # Contar las faltas del estudiante en cada materia
        total_faltas = asistencias.filter(materia=asistencia.materia, presente=False).count()

        # Crear o actualizar un reporte
        reporte, created = Reporte.objects.get_or_create(
            estudiante=asistencia.estudiante,
            materia=asistencia.materia,
            semestre=semestre,
            defaults={'total_faltas': total_faltas}
        )

        if not created:
            reporte.total_faltas = total_faltas
            reporte.save()

    return JsonResponse({"message": "Reportes generados correctamente"})


class GenerarReportePorEstudiante(APIView):
    def post(self, request, estudiante_id, semestre):
        # Llamamos a la función para generar reportes
        generar_reporte_por_estudiante(semestre, estudiante_id)
        return Response({"message": f"Reporte generado para el estudiante {estudiante_id} en el semestre {semestre}"})
    


    @action(detail=False, methods=['post'], url_path='generar-reporte/(?P<estudiante_id>\d+)/(?P<semestre>[^/.]+)')
    def generar_reporte(self, request, estudiante_id=None, semestre=None):
        # Llama a la función para generar el reporte
        mensaje = generar_reporte_por_estudiante(semestre, estudiante_id)
        return Response({"message": mensaje})

