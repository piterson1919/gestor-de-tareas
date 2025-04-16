from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Tareas
from .forms import TaskForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')


def registrarse(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username = request.POST['username'], password= request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tareas')
            except ValueError:
                return render(request, 'registro.html',{'form': UserCreationForm(),'error': ' El nombre de usuario ya existe'})
        elif request.POST['password1'] != request.POST['password2']:
            return render(request, 'registro.html', {'form': UserCreationForm(), 'error': 'Las contraseñas no coinciden'})

def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'iniciar_sesion.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'iniciar_sesion.html', {'form': AuthenticationForm(), 'error': 'Usuario o contraseña incorrectos'})
        else:
            login(request, user)
            return redirect('tareas')

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

@login_required
def tareas(request):
    tareas = Tareas.objects.filter(user=request.user, fecha_vencimiento__isnull=True)
    return render(request, 'tareas.html', {'tareas': tareas})

@login_required
def crear_tarea(request):
    if request.method == 'GET':
        return render(request, 'crear_tarea.html',{'form':TaskForm})
    else:
        form = TaskForm(request.POST)
        nueva_tarea = form.save(commit=False)
        nueva_tarea.user = request.user
        nueva_tarea.save()
        return redirect('tareas')

@login_required
def tarea_detalles(request, tarea_id):
    if request.method == 'GET':
        tarea = get_object_or_404(Tareas,pk=tarea_id,user=request.user)
        form = TaskForm(instance=tarea)
        return render(request,'tarea_detalles.html', {'tarea': tarea, 'form':form})
    else:
        try:
            tarea = get_object_or_404(Tareas, pk=tarea_id)
            form = TaskForm(request.POST, instance=tarea)
            form.save()
            return redirect('tareas')
        except ValueError:
            return render(request, 'tarea_detalles.html', {'tarea': tarea, 'form': form, 'error': 'Error al actualizar la tarea'})

@login_required
def borrar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, pk= tarea_id, user=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('tareas')
    
