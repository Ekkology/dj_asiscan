from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password',
            'date_joined'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True},  # Para evitar que el cliente envíe un valor
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(user_serializer, self).create(validated_data)
