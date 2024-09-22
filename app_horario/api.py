from rest_framework import permissions, viewsets
from .models import Estudiantes
from .serializer import HorarioSerializer


class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Estudiantes.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = HorarioSerializer
