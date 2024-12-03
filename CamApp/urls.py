# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import FaceRecognitionViewSet, FaceRecognitionView
from django.conf import settings
from django.conf.urls.static import static

# Configurar el router para las vistas de la API
router = DefaultRouter()
router.register(r'face-recognition2', FaceRecognitionViewSet, basename='face-recognition2')

# Definir las URL del proyecto
urlpatterns = [
    path('receive/', views.receive_image, name='receive_image'),
    path('display/', views.display_image, name='display_image'),
    path('display/enviar_valor_servos/', views.enviar_valor_servos, name='enviar_valor_servos'),
    path('display/manejar-direccion/', views.manejar_direccion, name='manejar_direccion'),
    path('view1/', views.display_image_view, name='display_image1'),
    path('api/face-recognition/', views.process_face_recognition, name='face_recognition_results'),
    path('face-recognition/', FaceRecognitionView.as_view(), name='face_recognition_results1'),
    path('api/', include(router.urls)),
]

# Agregar las URL para servir archivos est�ticos durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
