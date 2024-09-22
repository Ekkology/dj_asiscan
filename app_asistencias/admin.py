from django.contrib import admin
from .models import Asistencia
from .forms import AsistenciaForm

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    form = AsistenciaForm
    list_display = ('estudiante', 'materia_info', 'fecha_asistencia', 'hora_asistencia', 'asistio')
    list_filter = ('fecha_asistencia', 'asistio')
    search_fields = ('estudiante__nombre', 'codigo_hora__codigo_hora')
    ordering = ('-fecha_asistencia',)

    def materia_info(self, obj):
        return f"{obj.codigo_hora.id_materia.nombre_materia} - {obj.codigo_hora.dia_semana} - {obj.codigo_hora.salon} - {obj.codigo_hora.hora_inicio} a {obj.codigo_hora.hora_fin}"
    materia_info.short_description = 'Materia Info'

    def save_model(self, request, obj, form, change):
        # Aquí puedes agregar lógica adicional si es necesario
        super().save_model(request, obj, form, change)
