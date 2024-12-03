from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AsistenciaViewSet, registrar_asistencia

router = DefaultRouter()
router.register(r'asistenciasJSON', AsistenciaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('marcar_asistencia/', registrar_asistencia, name='registrar_asistencia'),
    
]

