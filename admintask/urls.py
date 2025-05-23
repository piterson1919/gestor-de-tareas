"""
URL configuration for admintask project.

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
from django.urls import path
from task import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('registrarse/',views.registrarse, name='registrarse'),
    path('iniciar_sesion/',views.iniciar_sesion, name='iniciar_sesion'),
    path('crear_tarea/',views.crear_tarea, name='crear_tarea'),
    path('tareas/',views.tareas, name='tareas'),
    path('tarea_detalles/<int:tarea_id>',views.tarea_detalles, name='tarea_detalles'),
    path('tarea_detalles/<int:tarea_id>/borrar',views.borrar_tarea, name='borrar_tarea'),
    path('cerrar_sesion/',views.cerrar_sesion, name='cerrar_sesion'),
]
