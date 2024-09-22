from django.urls import path
from . import views

urlpatterns = [
    path('receive/', views.receive_image, name='receive_image'),
    path('display/', views.display_image, name='display_image'),
    path('display/enviar_valor_servos/', views.enviar_valor_servos, name='enviar_valor_servos'),
    path('display/manejar-direccion/', views.manejar_direccion, name='manejar_direccion'),
    path('view1/', views.display_image_view, name='display_image1'),
]