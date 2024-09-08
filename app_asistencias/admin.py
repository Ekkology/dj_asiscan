from django.contrib import admin
from .models import Asistencia
from .forms import AsistenciaForm

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    form = AsistenciaForm
    list_display = ('estudiante', 'codigo_hora', 'fecha_asistencia', 'hora_asistencia', 'asistio')
    list_filter = ('fecha_asistencia', 'asistio')
    search_fields = ('estudiante__nombre', 'codigo_hora__codigo_hora')
    ordering = ('-fecha_asistencia',)

    def save_model(self, request, obj, form, change):
        # Aquí puedes agregar lógica adicional si es necesario
        super().save_model(request, obj, form, change)
