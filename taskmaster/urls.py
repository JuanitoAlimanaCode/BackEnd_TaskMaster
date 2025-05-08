"""
URL configuration for taskmaster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from taskmaster_det.views import *
from cuenta.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    #DRF
    path('api/espacios/',espaciosApiView.as_view(), name='api_espacios'),
    path('api/estados/',estadosApiView.as_view(), name='api_estados'),
    path('api/estadosxespacio/',EstadosPorEspacioApiView.as_view(), name='api_estados'),
    path('api/tareas/', tareasApiView.as_view(), name='api_tareas'),
    path('api/tareas/<int:espacio_id>/<int:estado_id>/', TareasPorEstadoListView.as_view()),

    path('api/espacios/<int:pk>/',espaciosUpdate.as_view(), name='api_espacios_update'),
    path('api/estados/<int:pk>/',estadosUpdate.as_view(), name='api_estados_update'),
    path('api/tareas/<int:pk>/',tareasUpdate.as_view(), name='api_tareas_update'),
    
    path('api/token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),

    path('api/registro/',RegistroView.as_view(), name='registro'),
    path('api/editarperfil/', editar_perfil, name='editarperfil'),
    path('api/validausuario/', VerificarUsuarioView.as_view(), name='validausuario'),
    path('api/cambiar-password/', cambiar_password, name='cambiar-password'),
    
    path('api/password-reset/', auth_views.PasswordResetView.as_view(email_template_name='cuenta/password_reset_email.html', success_url='/password-reset/done/'), name='password_reset'),
    path('api/password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('api/password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/password-reset/complete/'), name='password_reset_confirm'),
    path('api/password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
