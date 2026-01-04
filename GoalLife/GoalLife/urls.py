"""
URL configuration for GoalLife project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from Core import views
from rest_framework.authtoken import views as auth_views #Se lo importa asi para saber que son las vistas de autenticacion y no confundir con views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/login/', auth_views.obtain_auth_token),
    path('api/register/', views.api_registrar_usuario,name='api_registrar_usuario'), #Ruta para registrar una cuenta nueva
    #Home y datos
    path('api/home/', views.api_home, name='api_home'), #ruta para celular
    
    #Nueva Ruta
    path('api/metas/crear/', views.api_crear_meta, name='api_crear_meta'),
    path('api/gastos/crear/', views.api_crear_gasto, name='api_crear_gasto' ),
    path('api/metas/sumar/', views.api_sumar_ahorro, name='api_sumar_ahorro'),
    
    #Ruta de autenticacion y Perfil
    path('api/profile-summary/', views.UserProfileSummaryView.as_view(), name='profile_sumary'),   

    #Ruta para borrar registros
    path('api/metas/eliminar/<int:meta_id>/', views.api_eliminar_meta, name='api_eliminar_meta'),
    path('api/gastos/eliminar/<int:gasto_id>/', views.api_eliminar_gasto, name='api_eliminar_gasto'),

    #Para categorias
    path('api/categorias/', views.api_categorias, name='lista_categorias'),


]
