from rest_framework import permissions, viewsets
from .models import User
from .serializer import user_serializer


class user_viewset(viewsets.ModelViewSet):
   queryset =  User.objects.all()
   permissions_class = [permissions.AllowAny]
   serializer_class = user_serializer