from django.db import models

class Horario(models.Model):
    codigo_hora = models.CharField(max_length=10)
    id_materia = models.ForeignKey('Materias', on_delete=models.CASCADE)  # Nombre del modelo en plural
    id_carrera = models.ForeignKey('Carreras', on_delete=models.CASCADE)  # Nombre del modelo en plural
    id_facultad = models.ForeignKey('Facultades', on_delete=models.CASCADE)  # Nombre del modelo en plural
    dia_semana = models.CharField(max_length=10)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    salon = models.CharField(max_length=50)
    profesor = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo_hora} - {self.dia_semana} {self.hora_inicio} - {self.hora_fin}"


class Estudiantes(models.Model):
    id_estudiante = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Facultades(models.Model):
    id_facultad = models.AutoField(primary_key=True)
    nombre_facultad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_facultad


class Carreras(models.Model):
    id_carrera = models.AutoField(primary_key=True)
    nombre_carrera = models.CharField(max_length=100)
    id_facultad = models.ForeignKey(Facultades, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_carrera


class Materias(models.Model):
    id_materia = models.AutoField(primary_key=True)
    nombre_materia = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_materia


class CodigosHora(models.Model):
    id = models.AutoField(primary_key=True)
    codigo_hora = models.CharField(max_length=50)
    id_materia = models.ForeignKey(Materias, on_delete=models.CASCADE)
    id_carrera = models.ForeignKey(Carreras, on_delete=models.CASCADE)
    id_facultad = models.ForeignKey(Facultades, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=10)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    salon = models.CharField(max_length=50)
    profesor = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.codigo_hora} - {self.salon} - {self.profesor}'


class Matriculas(models.Model):
    id_estudiante = models.ForeignKey(Estudiantes, on_delete=models.CASCADE)
    id_codigo = models.ForeignKey(CodigosHora, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id_estudiante', 'id_codigo')


class MateriasCarreras(models.Model):
    id_materia = models.ForeignKey(Materias, on_delete=models.CASCADE)
    id_carrera = models.ForeignKey(Carreras, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id_materia', 'id_carrera')
