from django.urls import path, include
from . import views

app_name='djangoTareas'

urlpatterns = [
    path('',views.index,name='index'),
    path('cerrarSesion',views.cerrarSesion,name='cerrarSesion'),
    path('consolaAdministrador',views.consolaAdministrador,name='consolaAdministrador'),
    path('eliminarUsuario/<str:ind>',views.eliminarUsuario,name='eliminarUsuario'),
    path('verUsuario/<str:ind>',views.verUsuario,name='verUsuario'),
    path('nuevaTarea/<str:ind>',views.nuevaTarea,name='nuevaTarea'),
    path('eliminarTarea/<str:tareaId>&<str:usuarioId>',views.eliminarTarea,name='eliminarTarea'),
    path('finalizarTarea/<str:tareaId>&<str:usuarioId>',views.finalizarTarea,name='finalizarTarea'),
]
