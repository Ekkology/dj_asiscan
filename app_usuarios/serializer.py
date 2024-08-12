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