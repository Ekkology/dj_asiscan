from rest_framework import permissions, viewsets
from .models import User
from .serializer import user_serializer
from rest_framework.permissions import IsAuthenticated

class user_viewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]  # Requiere autenticación para acceder a esta vista
    serializer_class = user_serializer
