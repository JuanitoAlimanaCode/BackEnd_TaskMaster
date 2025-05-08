from rest_framework import serializers
from .models import *

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False}  # Ya no es estrictamente necesario como False, pero déjalo por claridad
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.get('username')  # Obtén el valor del username

        # Establece el email con el valor del username si no se proporcionó explícitamente
        if 'email' not in validated_data or not validated_data['email']:
            validated_data['email'] = username

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class perfilUsuarioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = perfilUsuario
        fields = '__all__'