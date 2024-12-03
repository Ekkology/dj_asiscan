from rest_framework import permissions, viewsets
from .models import User
from .serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated

class user_viewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]  # Requiere autenticación para acceder a esta vista
    serializer_class = UserSerializer



from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='admin').exists()

class IsProfessorUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='profesor').exists()

class AdminOnlyView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]  # Solo accesible para administradores
    serializer_class = UserSerializer

class ProfessorOnlyView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsProfessorUser]  # Solo accesible para profesores
    serializer_class = UserSerializer
