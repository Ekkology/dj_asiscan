from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializer import UserSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from .models import OutstandingToken
from django.contrib.auth.models import User
from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import UserSerializer


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Crear el token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            # Crear instancia de OutstandingToken
            outstanding_token = OutstandingToken.objects.create(user=user, token=access_token)

            # Obtener los grupos del usuario
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT group_id 
                    FROM auth_user_groups 
                    WHERE user_id = %s
                    """,
                    [user.id]
                )
                groups = [row[0] for row in cursor.fetchall()]
            
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "groups": groups,
                "token": access_token
            }
            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            
            # Si se actualizaron grupos, actualizar la tabla intermedia
            if 'groups' in request.data:
                with connection.cursor() as cursor:
                    # Primero eliminar todos los grupos existentes
                    cursor.execute(
                        "DELETE FROM auth_user_groups WHERE user_id = %s",
                        [user.id]
                    )
                    # Luego insertar los nuevos grupos
                    for group_id in request.data['groups']:
                        cursor.execute(
                            """
                            INSERT INTO auth_user_groups (user_id, group_id)
                            VALUES (%s, %s)
                            """,
                            [user.id, group_id]
                        )

            # Obtener los grupos actualizados
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT group_id 
                    FROM auth_user_groups 
                    WHERE user_id = %s
                    """,
                    [user.id]
                )
                groups = [row[0] for row in cursor.fetchall()]

            response_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "groups": groups
            }
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, user_id):
        return self.put(request, user_id)

class LoginUserView(APIView):
    def post(self, request):
        # Obtener las credenciales
        username = request.data.get('username')
        password = request.data.get('password')

        # Autenticar al usuario
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Si las credenciales son correctas, crear el token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Preparar la respuesta con los detalles del usuario y el token
            user_data = {
                "id": user.id,  # Agregar el ID del usuario
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "groups": [group.name for group in user.groups.all()],
                "token": access_token
            }

            return Response(user_data, status=status.HTTP_200_OK)

        # Si las credenciales son incorrectas
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    

# views.py
from django.contrib.auth.models import Group
from rest_framework import viewsets
from .serializer import GroupSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class LogoutUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Obtener el token de refresh del request
            refresh_token = request.data.get('refresh_token')
            
            if not refresh_token:
                return Response(
                    {'error': 'Es necesario el refresh token para cerrar sesi�n'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Obtener el token
            token = OutstandingToken.objects.filter(token=refresh_token).first()
            
            if token:
                # Si el token existe, lo agregamos a la lista negra
                BlacklistedToken.objects.get_or_create(token=token)
            
            return Response(
                {'message': 'Sesi�n cerrada exitosamente'},
                status=status.HTTP_200_OK
            )
            
        except TokenError as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Error al cerrar sesi�n'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )