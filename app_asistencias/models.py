from django.db import models
from app_horario.models import Estudiantes, CodigosHora

class Asistencia(models.Model):
    estudiante = models.ForeignKey(Estudiantes, on_delete=models.CASCADE)
    codigo_hora = models.ForeignKey(CodigosHora, on_delete=models.CASCADE)
    fecha_asistencia = models.DateField()
    hora_asistencia = models.TimeField()
    asistio = models.BooleanField()

    def __str__(self):
        return f"{self.estudiante.nombre} - {self.codigo_hora.codigo_hora} - {self.fecha_asistencia} - {'Asistió' if self.asistio else 'No asistió'}"
