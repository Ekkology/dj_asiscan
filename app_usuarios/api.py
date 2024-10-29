from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import user_serializer, LoginSerializer

class user_viewset(viewsets.ModelViewSet):
   queryset =  User.objects.all()
   permissions_class = [permissions.AllowAny]
   serializer_class = user_serializer
