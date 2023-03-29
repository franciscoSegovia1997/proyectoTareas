from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from .models import datosAdicionales, tareasInformacion
import datetime

# Create your views here.
def index(request):
    if request.method == "POST":
        nombreUsuario = request.POST.get('nombreUsuario')
        contraUsuario = request.POST.get('contraUsuario')
        usuarioInfo = authenticate(request,username=nombreUsuario,password=contraUsuario)
        if usuarioInfo is not None:
            login(request,usuarioInfo)
            if usuarioInfo.datosadicionales.tipoUsuario == 'ADMINISTRADOR':
                return HttpResponseRedirect(reverse("djangoTareas:consolaAdministrador"))
            else:
                return HttpResponseRedirect(reverse('djangoTareas:verUsuario', kwargs={'ind': usuarioInfo.id}))
        else:
            return HttpResponseRedirect(reverse("djangoTareas:index"))
    return render(request,'ingresoUsuario.html')

def cerrarSesion(request):
    logout(request)
    return HttpResponseRedirect(reverse("djangoTareas:index"))

def consolaAdministrador(request):
    if request.method == "POST":
        usernameUsuario = request.POST.get('usernameUsuario')
        contraUsuario = request.POST.get('contraUsuario')
        nombreUsuario = request.POST.get('nombreUsuario')
        apellidoUsuario = request.POST.get('apellidoUsuario')
        tipoUsuario = request.POST.get('tipoUsuario')
        nroCelular = request.POST.get('nroCelular')
        profesionUsuario = request.POST.get('profesionUsuario')
        perfilUsuario = request.POST.get('perfilUsuario')
        emailUsuario = request.POST.get('emailUsuario')
        usuarioCreado = User.objects.create(
            username=usernameUsuario,
            email=emailUsuario,
        )
        usuarioCreado.set_password(contraUsuario)
        usuarioCreado.first_name = nombreUsuario
        usuarioCreado.last_name = apellidoUsuario
        usuarioCreado.is_staff = True
        usuarioCreado.save()
        datosAdicionales.objects.create(
            user=usuarioCreado,
            tipoUsuario = tipoUsuario,
            nroCelular = nroCelular,
            profesionUsuario = profesionUsuario,
            perfilUsuario = perfilUsuario
        )
        return HttpResponseRedirect(reverse('djangoTareas:consolaAdministrador'))
    return render(request,'consolaAdministrador.html',{
        'usuariosTotales':User.objects.all().order_by('id'),
    })

def eliminarUsuario(request,ind):
    usuarioEliminar = User.objects.get(id=ind)
    datosEliminar = datosAdicionales.objects.get(user=usuarioEliminar)
    datosEliminar.delete()
    usuarioEliminar.delete()
    return HttpResponseRedirect(reverse('djangoTareas:consolaAdministrador'))

def verUsuario(request,ind):
    usuarioInfo = User.objects.get(id=ind)
    tareasUsuario = tareasInformacion.objects.filter(usuarioRelacionado=usuarioInfo).order_by('id')
    return render(request,'informacionUsuario.html',{
        'usuarioInfo':usuarioInfo,
        'tareasUsuario':tareasUsuario,
    })

def nuevaTarea(request, ind):
    if request.method == 'POST':
        usuarioRelacionado = User.objects.get(id=ind)
        fechaInicio = request.POST.get('fechaInicio')
        fechaFin = request.POST.get('fechaFin')
        descripcionTarea = request.POST.get('descripcionTarea')
        fechaSeparada = fechaInicio.split('-')
        ini_dia = int(fechaSeparada[2])
        ini_mes = int(fechaSeparada[1])
        ini_anho = int(fechaSeparada[0])
        fechaSeparada = fechaFin.split('-')
        fin_dia = int(fechaSeparada[2])
        fin_mes = int(fechaSeparada[1])
        fin_anho = int(fechaSeparada[0])
        tareasInformacion.objects.create(
            fechaInicio=datetime.datetime(ini_anho,ini_mes,ini_dia),
            fechaFin=datetime.datetime(fin_anho,fin_mes,fin_dia),
            descripcionTarea=descripcionTarea,
            usuarioRelacionado=usuarioRelacionado
        )
        return HttpResponseRedirect(reverse('djangoTareas:verUsuario', kwargs={'ind': ind}))
    
def eliminarTarea(request,tareaId,usuarioId):
    tareaEliminar = tareasInformacion.objects.get(id=tareaId)
    tareaEliminar.delete()
    return HttpResponseRedirect(reverse('djangoTareas:verUsuario', kwargs={'ind': usuarioId}))

def finalizarTarea(request,tareaId,usuarioId):
    tareaFinalizar = tareasInformacion.objects.get(id=tareaId)
    tareaFinalizar.estadoTarea = 'TERMINADA'
    tareaFinalizar.save()
    return HttpResponseRedirect(reverse('djangoTareas:verUsuario', kwargs={'ind': usuarioId}))