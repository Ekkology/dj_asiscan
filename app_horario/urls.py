from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstudiantesViewSet

router = DefaultRouter()
router.register(r'estudiantes', EstudiantesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
