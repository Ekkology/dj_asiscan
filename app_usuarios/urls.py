from os import path
from rest_framework import routers
from .api import user_viewset,LoginViewSet



router = routers.DefaultRouter()

router.register('api/users',user_viewset,'User')


urlpatterns = router.urls
# Agregar la URL para el login manualmente
urlpatterns = router.urls + [
    path('api/login/', LoginViewSet.as_view({'post': 'create'}), name='login'),
]