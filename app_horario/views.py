from rest_framework import viewsets
from .models import Estudiantes
from .serializer import EstudiantesSerializer 

class EstudiantesViewSet(viewsets.ModelViewSet):
    queryset = Estudiantes.objects.all()
    serializer_class = EstudiantesSerializer
