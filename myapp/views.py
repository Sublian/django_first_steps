from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
import calendar
import locale
from .models import Proyect, Task
from .forms import CreateNewProyect, TaskForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    title = "Django Course!!!"
    return render(request, 'index.html',
                  {'title': title})


def hello(request, username):
    print(f"variable recibida: username-->{username} de tipo {type(username)}")
    # username= username.upper()
    # return HttpResponse("<h1>hello mister %s</h1>" %username.upper())
    return HttpResponse("<h1>hello mister %s</h1>" % username.capitalize())


def about(request):
    username = "Sublian"
    return render(request, 'about.html',
                  {'username': username})


def other(request):
    """
    url_completa = request.build_absolute_uri()
    print("url  desde other-->", url_completa)
    print(obtener_nombre_mes_y_anio(int(url_completa.split("D")[1][:2])))
    """
    return HttpResponse("<h1>Just other page</h1>")


"""def proyects(request):
    proyectos = list(Proyect.objects.values())
    return JsonResponse(proyectos, safe=False)"""

@login_required
def proyects(request):
    proyects = list(Proyect.objects.values())
    return render(request, "proyects/proyects.html",
                  {"proyects": proyects})

@login_required
def tasks(request):
    #tasks = Task.objects.all() muestra todas las tareas sin filtrar
    #muestra por usuario y si datecompleted no es nulo
    tasks = Task.objects.filter(user=request.user,  datecompleted__isnull=False)
    return render(request, "tasks/tasks.html",
                  {"tasks": tasks})

""" version original
def create_task(request):
    if request.method == 'GET':
        return render(request, 'tasks/create_task.html', {'form': CreateNewTask()})
    else:
        Task.objects.create(
            title=request.POST['title'], description=request.POST['description'], proyect_id=2)
        return redirect('tasks')"""

@login_required
def create_task(request):
    if request.method == 'GET':        
        return render(request, 'tasks/create_task.html', {'form': TaskForm})
    try:
        
        form=TaskForm(request.POST)
        new_task=form.save(commit=False)
        new_task.user=request.user
        new_task.save()
        return redirect('tasks')
    except:
        return render(request, 'tasks/create_task.html', {'form': TaskForm, 'error': '<Error creating task!>'})        

@login_required    
def create_proyect(request):
    if request.method == 'GET':
        return render(request, 'proyects/create_proyect.html', {'form': CreateNewProyect()})
    else:

        Proyect.objects.create(
            name=request.POST['name'])
        return redirect('proyects')

@login_required
def proyect_detail(request, id):
    proyect = get_object_or_404(Proyect, id=id)
    tasks = Task.objects.filter(proyect_id=id)
    print(tasks)
    return render(request, 'proyects/detail.html', {
        'proyect': proyect,
        'tasks': tasks
    })

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task,pk=task_id, user = request.user)
    if request.method == 'GET':        
        
        form = TaskForm(instance=task)
        return render(request, 'tasks/detail.html', {'task':task, 'form': form})
    else:
        try:        
            
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/detail.html', {'task':task, 'form': form, 'error': 'Error Updating Task'})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False)#.order_by('-datecompleted')
    return render(request, 'tasks/tasks.html',
                  {'tasks': tasks})

@login_required    
def complete_task(request,task_id):
    task = get_object_or_404(Task, pk = task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('task')

@login_required    
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user=request.user)
    if request.method == 'POST':        
        task.delete()
        return redirect('task')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1']== request.POST['password2']:
            try:
                user= User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', 
                              {'form': UserCreationForm, 
                               'error': 'Username already exists!'})
        return render(request, 'signup.html', 
                      {'form': UserCreationForm, 
                        'error': 'Passwords do not match!'})


def home(request):
    return render(request, 'home.html')

@login_required
def signout(request):
    logout(request)
    return redirect('index')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:        
        user=authenticate(request, username=request.POST['username'], password=request.POST['password']) 
         
        if user is None:
            return render(request,'signin.html', 
                        {'form': AuthenticationForm, 
                        'error': 'Username or password is incorrect'})
        else:
            login(request, user)
            return redirect('tasks')
        