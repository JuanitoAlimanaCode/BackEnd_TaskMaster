from rest_framework import serializers
from .models import *

#Api Espacios
class espaciosSerializer(serializers.ModelSerializer):

    class Meta:
        model = espacios
        fields = '__all__'

#Api Estados
class estadosSerializer(serializers.ModelSerializer):

    espacio = serializers.SerializerMethodField()
    espacio_id = serializers.PrimaryKeyRelatedField(
        source='espacio',
        queryset=espacios.objects.all(),
        write_only=True
    )

    class Meta:
        model = estados
        fields = '__all__'

    def get_espacio(self, obj):
        return {
            'id': obj.espacio.id,
            'nombre': obj.espacio.espacio
        }
    
#Api Tareas
class tareasSerializer(serializers.ModelSerializer):

    espacio_id = serializers.PrimaryKeyRelatedField(
        queryset=espacios.objects.all(),
        source='espacio',
        write_only=True,
        required=True
    )
    estado_id = serializers.PrimaryKeyRelatedField(
        queryset=estados.objects.all(),
        source='estado',
        write_only=True,
        required=True
    )

    espacio = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()

    class Meta:
        model = tareas
        fields = '__all__'

    def get_espacio(self, obj):
        return {
            'id': obj.espacio.id,
            'nombre': obj.espacio.espacio
        }

    def get_estado(self, obj):
        return {
            'id': obj.estado.id,
            'estado': obj.estado.estado
        }
    
