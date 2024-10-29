#from os import path
from rest_framework import routers
from .api import user_viewset
from . import views 
from django.urls import path, re_path


router = routers.DefaultRouter()

router.register('api/users',user_viewset,'User')


urlpatterns = router.urls

# Agregar la URL para el login 
urlpatterns = router.urls + [
    path('login',views.login), #se puede añadir la misma logica de rutas para registro y perfil 
]