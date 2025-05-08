from django.db import models
from django.contrib.auth.models import User  
from django.utils.timezone import now 
from django.db.models import Q

import datetime
from django.utils import timezone
from django.db import models

# Create your models here.
class espacios(models.Model):
    espacio = models.CharField(verbose_name="Espacio",max_length=50, null=False, blank=False)
    usuario = models.CharField(verbose_name="Usuario",max_length=50, null=False, blank=False, default='usuario_por_defecto')
    fecha_creacion = models.DateField(verbose_name="Fecha de Creación", auto_now_add=True)
    fecha_actualizacion = models.DateField(verbose_name="Fecha de Actualización", auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = 'Espacio'
        verbose_name_plural = 'Espacios'

    def __str__(self):
        return self.espacio
    
class estados (models.Model):
    estado = models.CharField(verbose_name="Estado",max_length=50, null=False, blank=False)
    espacio = models.ForeignKey(espacios, on_delete=models.CASCADE, verbose_name="Espacio")
    fecha_creacion = models.DateField(verbose_name="Fecha de Creación", auto_now_add=True)
    fecha_actualizacion = models.DateField(verbose_name="Fecha de Actualización", auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return self.estado

def default_fecha_vencimiento():
    
    return timezone.now().date() + datetime.timedelta(days=7)

class tareas (models.Model):
    tarea = models.CharField(verbose_name="Tarea",max_length=50, null=False, blank=False)
    estado = models.ForeignKey(estados, on_delete=models.CASCADE, verbose_name="Estado")
    espacio = models.ForeignKey(espacios, on_delete=models.CASCADE, verbose_name="Espacio")
    descripcion = models.CharField(verbose_name="Detalle",max_length=50, null=False, blank=True)
    fecha_vencimiento = models.DateField(default=default_fecha_vencimiento)
    prioridad = models.IntegerField(verbose_name="Prioridad", default=1, null=False, blank=False)
    categoría = models.CharField(verbose_name="Categoría",max_length=50, null=False, blank=True)
    fecha_creacion = models.DateField(verbose_name="Fecha de Creación", auto_now_add=True)
    fecha_actualizacion = models.DateField(verbose_name="Fecha de Actualización", auto_now=True)

    class Meta: 
        ordering = ["id"]    
        verbose_name = 'Tarea'        
        verbose_name_plural = 'Tareas'          

    def __str__(self):
        return self.tarea
