from .models import reporte
from rest_framework import viewsets, permissions
from .serializers import ReporteSerializer

class ReporteViewSet(viewsets.ModelViewSet):
    queryset = reporte.objects.all() # conjunto de datos - consultas SQL
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ReporteSerializer.ReporteSerializer

    


