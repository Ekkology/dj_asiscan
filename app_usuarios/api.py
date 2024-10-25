from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import user_serializer, LoginSerializer

class user_viewset(viewsets.ModelViewSet):
   queryset =  User.objects.all()
   permissions_class = [permissions.AllowAny]
   serializer_class = user_serializer


   class LoginViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]  # Permitir acceso a cualquier usuario

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(username=username)
                
                # Verificar la contraseña 
                if user.password == password:  # Cambiar a un método seguro en producción
                    return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
            except User.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)