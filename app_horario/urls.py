from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstudiantesViewSet
from . import views

router = DefaultRouter()
router.register(r'estudiantesJSON', EstudiantesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('estudiantes/<int:id_estudiante>/', views.estudiante_detalle, name='estudiante_detalle'),
    path('login/', views.login_view, name='login'),
    path('horario/<int:id_estudiante>/', views.horario_estudiante, name='horario_estudiante'),
]
