from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import user_serializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAutentication
#api view post para login 
@api_view(['POST'])
def login(request):

   user =  get_object_or_404(User,username=request.data['username'])

   if not user.check_password(request.data['password']):
        return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
   token, created = Token.objects.get_or_create(user=user)
   serializer = user_serializer(instance=user)
   
   return Response({"token": token.key, "user": created})

#api view post para registro
@api_view(['POST'])
def register(request):
    serializer = user_serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=serializer.data['username']).set_password(request.data['password'])
        user.set_password(serializer.data['password'])
        user.save()

        token = Token.objects.create(user=user)
        return Response ({'token': token.key, 'user': serializer.data},status=status.HTTP_200_OK)
  
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#api view para perfil

@api_view(['POST'])
@authentication_classes([TokenAutentication])
@permission_classes([IsAuthenticated])
def profile(request):
    print(request.user)

    return Response("You are login with {}".format(request.user.user.username), stattus=status.HTTP_200_OK)
