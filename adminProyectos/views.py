from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Proyecto
from django.contrib.auth.models import User


def home(request):
    title = "Inicio"

    data = {
        "title" : title,
    }

    return render(request, 'adminProyectos/home.html',data)

def proyectos(request):
    proyectos = Proyecto.objects.all()
    temas = Proyecto.objects.values_list('tema', flat=True).distinct()
    tema_seleccionado = request.GET.get('tema')
    if tema_seleccionado:
        proyectos = proyectos.filter(tema=tema_seleccionado)
    return render(request, 'adminProyectos/proyectos.html', {'proyectos': proyectos, 'temas': temas, 'tema_seleccionado': tema_seleccionado})

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Nombre de usuario o contraseña incorrectos.'
            
    return render(request, 'adminProyectos/login.html', {'error_message': error_message})

@login_required
def crearNuevoProyecto(request):  
    if request.method == 'POST':
        nombre_proyecto = request.POST.get('nombre_proyecto', request.POST.get('tema', ''))
        estudiante = request.user.get_full_name()
        tema = request.POST.get('tema', '')
        profesor = request.POST.get('profesor', '')
        Proyecto.objects.create(nombre_proyecto=nombre_proyecto, estudiante=estudiante, tema=tema, profesor=profesor, usuario=request.user)
        return redirect('proyectos')
    
    profesores = User.objects.filter(groups__name='profesor')
    return render(request, 'adminProyectos/nuevoproyecto.html', {'profesores': profesores})

@login_required
def verProyectos(request):
    es_profesor = request.user.groups.filter(name='profesor').exists()
    
    if es_profesor:
        proyectos = Proyecto.objects.all()
        tema_filtrado = request.GET.get('tema')
        if tema_filtrado:
            proyectos = proyectos.filter(tema=tema_filtrado)
        
        proyectos_sin_profesor = proyectos.filter(profesor='')
        
        if request.method == 'POST':
            proyectos_seleccionados = request.POST.getlist('proyectos_seleccionados')
            profesor_asignado = request.user.get_full_name()
            for proyecto_id in proyectos_seleccionados:
                proyecto = Proyecto.objects.get(id=proyecto_id)
                proyecto.profesor = profesor_asignado
                proyecto.save()
            return redirect('proyectos')
        
        return render(request, 'adminProyectos/verProyectos.html', {'proyectos': proyectos, 'tema_filtrado': tema_filtrado, 'proyectos_sin_profesor': proyectos_sin_profesor})
    else:
        return redirect('proyectos')