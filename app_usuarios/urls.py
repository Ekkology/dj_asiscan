from django.urls import path
from rest_framework import routers
from .api import user_viewset
from .views import RegisterUserView, LoginUserView, LogoutUserView, GroupViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Crea el enrutador y registra las vistas que son ViewSet
router = routers.DefaultRouter()
router.register('api/users', user_viewset, 'User')
router.register('api/groups', GroupViewSet, 'Group')
# Elimina esta l�nea: router.register('api/logout', LogoutUserView , 'Logout')

# Define las rutas para las vistas basadas en APIView
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterUserView.as_view(), name='register_user'),
    path('api/login/', LoginUserView.as_view(), name='login_user'),
    path('api/register/<int:user_id>/', RegisterUserView.as_view(), name='update-user'),
    path('api/logout/', LogoutUserView.as_view(), name='logout'),  # Cambiado a /api/logout/ para mantener consistencia
]

# Agrega las rutas del enrutador
urlpatterns += router.urls