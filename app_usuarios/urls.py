from django.urls import path
from rest_framework import routers
from .api import user_viewset  # Importa tu ViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterUserView
from .views import LoginUserView
# Crea el enrutador y registra la vista de usuario
router = routers.DefaultRouter()
router.register('api/users', user_viewset, 'User')

# Define las rutas para las vistas de obtención y actualización de tokens JWT
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterUserView.as_view(), name='register_user'),
    path('api/login/', LoginUserView.as_view(), name='login_user'),
]

# Agrega las rutas del enrutador al patrón de URL final
urlpatterns += router.urls
