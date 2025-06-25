from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User  
from django.contrib.auth import authenticate, login, logout  
from .models import Task
from .forms import Taskform
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')

def loguin(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
        if user is None:
            return render(request, 'login.html', { 'error': 'Usuario o contraseña incorrectos'})
        else:
            login(request, user)
            return redirect('tasks')
        
def register(request):
    if request.method == 'GET':
        return render (request,'register.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                login(request, user)
                user.save()
                return redirect('tasks')
            except:
                return render(request, 'register.html', {'error': 'nombre de usuario ya existente'})
        else:
            return render(request, 'register.html', {'error': 'las contraseñas no coinciden'})
        
@login_required
def tasks(request):
        tasks = Task.objects.filter(user=request.user)
        return render(request,'tasks.html',{'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': Taskform()})
    else:
        form = Taskform(request.POST)
        nueva_tarea = form.save(commit=False)
        nueva_tarea.user = request.user
        nueva_tarea.save()
        return redirect('tasks')

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        form = Taskform(instance=task)
        return render(request, 'task_detail.html', {'form': form, 'task': task})
    else:
        try:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            form = Taskform(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'form': form, 'task': task, 'error': 'error al actualizar la tarea'})

@login_required
def delete_task(request,task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
def singout(request):
    logout(request)
    return redirect('home')