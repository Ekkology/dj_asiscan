from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AsistenciaViewSet

router = DefaultRouter()
router.register(r'asistenciasJSON', AsistenciaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]