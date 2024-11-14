"""
URL configuration for dj_asiscan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .view import home, simulate
#from .view import obtener_imagen
from CamApp import urls as cam_urls
from .view import github_webhook
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home),
    path('sim/',simulate),
    path('users/', include('app_usuarios.urls') ),
    path('cam/', include(cam_urls)),  # Ruta de la rama orlando_branch
    path('horario/', include('app_horario.urls')),  # Ruta de la rama main
    path('asistencias/', include('app_asistencias.urls')),  # Ruta de la rama main
    #path('obtener_imagen/', obtener_imagen ),
    path('hook_1/', github_webhook ),
]
