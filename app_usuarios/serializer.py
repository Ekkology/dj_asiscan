from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.db import connection
from .models import User

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password',
            'date_joined',
            'groups'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True},
        }

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        validated_data['password'] = make_password(validated_data['password'])
        user = super(UserSerializer, self).create(validated_data)

        # Insertar directamente en la tabla auth_user_groups si hay grupos
        if groups:
            with connection.cursor() as cursor:
                for group_id in groups:
                    cursor.execute(
                        """
                        INSERT INTO auth_user_groups (user_id, group_id)
                        VALUES (%s, %s)
                        """,
                        [user.id, group_id]
                    )

        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Obtener los grupos directamente de la base de datos
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT group_id 
                FROM auth_user_groups 
                WHERE user_id = %s
                """,
                [instance.id]
            )
            groups = [row[0] for row in cursor.fetchall()]
            
        representation['groups'] = groups
        return representation

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'