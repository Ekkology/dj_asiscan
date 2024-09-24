from rest_framework  import serializers
from models import reportes 


class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = reportes
        fields = ('id_reporte', 'nombre', 'fecha', 'tipo', 'descripcion', 'usuario', 'imagen','comentarios')
        read_only_fields = ('id_reporte',) #buscar para que es el read only fields
        



    
    
    
