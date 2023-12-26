from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import UserLoginForm, UserSignUpForm
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import JsonResponse
from django.core.paginator import Paginator
#Imports Admin
from .models import Mensaje, Calendario, Cursos, Eventos, Actividad
from .forms import Messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request,"core/index.html")

def cursos(request):
    cur=Cursos.objects.all()
    paginator = Paginator(cur,2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "core/cursos.html", {'cur': page_obj})

def eventos(request):
    eve=Eventos.objects.all()
    paginator = Paginator(eve,1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "core/eventos.html", {'eve': page_obj})

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



def contactoF(request):
    return render(request, "core/contactoF.html")

def logout_view(request):
    logout(request)
    return redirect('index')

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
            return redirect('index')
        else:
            messages.warning(
                request, 'Correo Electronico o Contrasena invalida')
            return redirect('index')

    messages.error(request, 'Formulario Invalido')
    return redirect('index')


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
            Actividad.objects.create(sender=user,verb="se ha registrado")
            return redirect('index')

        except Exception as e:
            print(e)
            return JsonResponse({'detail': f'{e}'})



def inbox(request):
    messages = Mensaje.objects.raw('select b.id , a.nombre,a.correo,b.asunto,b.mensaje,b.creado from core_userprofile a,core_mensaje b where a.nombre = remitente_id')
    return render(request,'admin/inbox.html',{'messages': messages})

# Vista que envia el mensaje del formulario
@login_required(login_url="/formulario/")
def enviar_mensaje(request):
    if request.method == 'POST':
        form = Messages(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.remitente = request.user
            mensaje.save()
    else:
        form = Messages()

    return render(request, 'core/contactoF.html', {'form': form})

def eliminar_mensaje(request):
    if request.method == 'POST':
        id = request.POST['message_id']
        msg = get_object_or_404(Mensaje, pk=id)
        msg.delete()
        return redirect('inbox')

#Vistas Admin

# Vista para responder y enviar el mensaje
def responder_mensaje(request):
    if request.method == "POST":
        nombre = request.POST['nombre']
        asunto = request.POST['asunto']
        correo = request.POST['correo']
        mensaje = request.POST['mensaje']

        template = render_to_string('email_template.html',{
            'correo' : correo,
            'mensaje' : mensaje
        })

        correo = EmailMessage(
            asunto,
            template,
            settings.EMAIL_HOST_USER,
            [correo]
        )

        correo.fail_silently = False
        correo.send()

        messages.success(request,"Se ha enviado tu correo")
        return redirect('inbox')


@login_required(login_url="/admin/login/")
def activity(request):
    act = Actividad.objects.all()
    return render(request, 'admin/activity.html',{'act':act })

@login_required(login_url="/admin/login/")
def calendar(request):
    all_calendar = Calendario.objects.all()
    context = {
        "calendar" : all_calendar
    }
    return render(request, 'admin/calendario.html', context)

def all_calendar(request):
    all_calendar = Calendario.objects.all()
    out = []
    for event in all_calendar:
        out.append({
            'title' : event.nombre,
            'id' : event.id,
            'start' : event.fechayhora.strftime("%m/%d/%Y %H:%M:%S"),
        })
    return JsonResponse(out, safe = False)