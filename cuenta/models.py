from django.db import models
from django.contrib.auth.models import User

# Create your models here.
url_ruta = 'static/assets/images'

class perfilUsuario(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='perfilUsuario')
    avatar = models.ImageField(upload_to=f'{url_ruta}/perfil', null=True, blank=True)
    telefono = models.CharField(verbose_name="Teléfono", max_length=15, null=True, blank=True)
    direccion = models.CharField(verbose_name="Dirección", max_length=100, null=True, blank=True)
    descripcion = models.CharField(verbose_name="Descripción", max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)

    def __str__ (self):
        return self.user.username

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'
