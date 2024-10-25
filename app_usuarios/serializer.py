from rest_framework import serializers
from .models import User

class user_serializer(serializers.ModelSerializer):
    class Meta:
          model = User
          fields = [
            'id', 
            'password', 
            'last_login', 
            'is_superuser', 
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'is_staff', 
            'is_active', 
            'date_joined'
        ]
          extra_kwargs = {
            'password': {'write_only': True},
        }
          
#Serializer para el login
class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Campo de solo escritura

    class Meta:
        model = User
        fields = ['username', 'password']


#Si no funciona usar este:
#class LoginSerializer(serializers.Serializer):
 #   username = serializers.CharField(required=True)
  #  password = serializers.CharField(required=True)