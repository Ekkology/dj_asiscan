from rest_framework  import serializers
from .models import Reporte


class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = ('estudiante','materia','total_faltas','semestre')
        read_only_fields = ('total_faltas',) 
        



    
    
