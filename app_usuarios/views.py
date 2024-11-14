from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializer import user_serializer
from django.contrib.auth import authenticate
class RegisterUserView(APIView):
    def post(self, request):
        serializer = user_serializer(data=request.data)
        role = request.data.get('role')  # Obtener el rol del request

        if serializer.is_valid():
            # Guardar el usuario
            user = serializer.save()

            # Asignar grupo basado en el rol
            if role:
                try:
                    group = Group.objects.get(name=role)
                    user.groups.add(group)
                except Group.DoesNotExist:
                    return Response({'detail': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

            # Crear el token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Incluir el token en la respuesta
            response_data = serializer.data
            response_data['token'] = access_token  # Añadir el token a la respuesta

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Autenticar al usuario con el username y password
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Si el usuario existe y las credenciales son correctas
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Retornamos el token de acceso
            return Response({
                'username': user.username,
                'token': access_token
            }, status=status.HTTP_200_OK)

        # Si las credenciales son incorrectas
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)