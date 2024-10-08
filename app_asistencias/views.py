from rest_framework import viewsets
from .models import Asistencia
from .serializer import AsistenciaSerializer

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
