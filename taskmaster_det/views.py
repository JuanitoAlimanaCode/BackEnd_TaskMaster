from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import generics
from .serializers import *

# Create your views here.

### Vista Espacios ###
class espaciosApiView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
        espacio = espacios.objects.filter(usuario=request.user)
        serializer = espaciosSerializer(espacio, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = espaciosSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            
            espacio_guardado = serializer.save()
            return Response({
                "id": espacio_guardado.id,
                **serializer.data 
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class espaciosUpdate(APIView):

    permissionclasses = [IsAuthenticated]

    def put(self, request, pk):
        
        espacio = get_object_or_404(espacios, pk=pk)
        if espacio is not None:
            serializer = espaciosSerializer(espacio, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Espacio no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            espacio = espacios.objects.get(pk=pk) 
            espacio.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except espacios.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error al eliminar el espacio: {e}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
### Vista Estados ###
class estadosApiView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        espacio = espacios.objects.all()
        serializer = estadosSerializer(espacio, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = estadosSerializer(data=request.data)

        if serializer.is_valid():
            estado_guardado = serializer.save()
            return Response({
                **serializer.data,
                "id": estado_guardado.id,
                
            }, 
            status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class estadosUpdate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def put(self, request, pk):
        estado = get_object_or_404(estados, pk=pk)  

        try:
            espacio_obj = espacios.objects.get(pk=request.data['espacio']) 
            estado.espacio = espacio_obj
            data = request.data.copy()

            serializer = estadosSerializer(estado, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except espacios.DoesNotExist:
            return Response({'message': 'Espacio no encontrado.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error al actualizar el estado: {e}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        try:
            estado = estados.objects.get(pk=pk) 
            estado.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except estados.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error al eliminar el estado: {e}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def obtener_estados_por_espacio(request, espacio_id):

    estados = estados.objects.filter(espacio_id=espacio_id)
    serializer = estadosSerializer(estados, many=True)
    return Response(serializer.data)

### Vista Estados por Espacio ###
class EstadosPorEspacioApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        espacio_id_str = request.query_params.get('espacioId')
        print(f"espacioId recibido: {espacio_id_str} (Tipo: {type(espacio_id_str)})")

        if espacio_id_str:
            try:
                espacio_id = int(espacio_id_str) # ¡Esta es la conversión correcta!
                print(f"espacioId convertido a entero: {espacio_id} (Tipo: {type(espacio_id)})")
                estados_queryset = estados.objects.filter(espacio=espacio_id)
                serializer = estadosSerializer(estados_queryset, many=True)
                print(f"Estados serializados: {serializer.data}")
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({"error": "El parámetro espacioId debe ser un entero"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Se requiere el parámetro espacioId"}, status=status.HTTP_400_BAD_REQUEST)
### Vista Tareas ###
class tareasApiView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tareas = tareas.objects.all()
        serializer = tareasSerializer(tareas, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        print("Datos recibidos:", request.data) 
        serializer = tareasSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Errores:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class tareasUpdate(APIView):
    permissionclasses = [IsAuthenticated]

    def put(self, request, pk):
        tareas_obj = get_object_or_404(tareas, pk=pk)

        try:
            espacio_id = request.data.get('espacio')
            if espacio_id:
                espacio_obj = espacios.objects.get(pk=espacio_id)
                tareas_obj.espacio = espacio_obj
        except espacios.DoesNotExist:
            return Response({'message': 'Espacio no encontrado.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            estado_id = request.data.get('estado')
            if estado_id:
                estado_obj = estados.objects.get(pk=estado_id)
                tareas_obj.estado = estado_obj
        except estados.DoesNotExist:
            return Response({'message': 'Estado no encontrado.'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        serializer = tareasSerializer(tareas_obj, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        tarea = get_object_or_404(tareas, pk=pk) #linea194
        tarea.delete()
        return Response({'message': 'Tarea eliminada.'}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def obtener_tareas_por_estado(request, espacio_id, estado_id):

    tarea = tareas.objects.filter(espacio_id=espacio_id, estado_id=estado_id)
    serializer = tareasSerializer(tarea, many=True)
    return Response(serializer.data)

### Filtro Tareas por Estado ###
class TareasPorEstadoListView(generics.ListAPIView):
    serializer_class = tareasSerializer

    def get_queryset(self):
        espacio_id = self.kwargs.get('espacio_id')
        estado_id = self.kwargs.get('estado_id')
        if espacio_id and estado_id:
            return tareas.objects.filter(espacio_id=espacio_id, estado_id=estado_id)
        return tareas.objects.none()
    
################################
###    CAMBIAR CONTRASEÑA    ###
################################

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def cambiar_password(request):
    usuario = request.user
    datos = request.data

    actual = datos.get('password_actual')
    nueva = datos.get('nueva_password')
    confirmar = datos.get('confirmar_password')

    if not usuario.check_password(actual):
        return Response({"error": "La contraseña actual es incorrecta."}, status=status.HTTP_400_BAD_REQUEST)

    if nueva != confirmar:
        return Response({"error": "Las contraseñas nuevas no coinciden."}, status=status.HTTP_400_BAD_REQUEST)

    if len(nueva) < 6:
        return Response({"error": "La nueva contraseña debe tener al menos 6 caracteres."}, status=status.HTTP_400_BAD_REQUEST)

    usuario.set_password(nueva)
    usuario.save()

    return Response({"mensaje": "Contraseña cambiada con éxito."}, status=status.HTTP_200_OK)