from django.shortcuts import render

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