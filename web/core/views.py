from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import UserLoginForm, UserSignUpForm
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import HttpResponse, JsonResponse

# Create your views here.

def index(request):
    return render(request,"core/index.html")

def cursos(request):
    return render(request, "core/cursos.html")

def eventos(request):
    return render(request, "core/eventos.html")

def recursos(request):
    return render(request, "core/recursos.html")

def testimonios(request):
    return render(request, "core/testimonios.html")

def galeria(request):
    return render(request, "core/galeria.html")

def cyp(request):
    return render(request, "core/cyp.html")

def formulario(request):
    return render(request, "core/login.html")

def register(request):
    return render(request, "core/register.html")



# Codigo agustin

def login_view(request):
    login_form = UserLoginForm(request.POST or None)
    if login_form.is_valid():
        nombre = login_form.cleaned_data.get('nombre')
        correo = login_form.cleaned_data.get('correo')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request,nombre=nombre, correo=correo, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Has iniciado sesion correctamente')
            return redirect('home')
        else:
            messages.warning(
                request, 'Correo Electronico o Contrasena invalida')
            return redirect('home')

    messages.error(request, 'Formulario Invalido')
    return redirect('home')


def signup_view(request):
    signup_form = UserSignUpForm(request.POST or None)
    if signup_form.is_valid():
        nombre = signup_form.cleaned_data.get('nombre')
        correo = signup_form.cleaned_data.get('correo')
        password = signup_form.cleaned_data.get('password')
        try:
            user = get_user_model().objects.create(
                nombre=nombre,
                correo=correo,
                password=make_password(password),
                is_active=True
            )
            login(request, user)
            return redirect('home')

        except Exception as e:
            print(e)
            return JsonResponse({'detail': f'{e}'})

def logout_view(request):
    logout(request)
    return redirect('home')