from django.db import models

#Los estudiantes y materias forman parte de la otra app_horario y materias que se creo 
class Reporte(models.Model):
    estudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE)
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE)
    total_faltas = models.IntegerField()
    semestre = models.CharField(max_length=20)

    def __str__(self):
        return f'Reporte de {self.estudiante.nombre} en {self.materia.nombre} ({self.semestre})'


