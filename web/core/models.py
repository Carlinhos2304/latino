from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin , BaseUserManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import gettext_lazy as _


#UserManager
class CustomAccountManager(BaseUserManager):
    def create_user(self, nombre, correo,  password, **other_fields):

        if not correo:
            raise ValueError(_('You must provide an email address'))

        correo = self.normalize_email(correo)
        user = self.model(correo=correo, nombre=nombre,
                        **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, nombre, correo,  password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(nombre, correo, password, **other_fields)

#Modelo Perfil

class UserProfile(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(primary_key=True,unique=True, max_length=100)
    correo = models.EmailField(_('email address'), unique=True)
    creado = models.DateTimeField(auto_now_add=True)

    register_date = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'nombre'
    REQUIRED_FIELDS = ['correo']

    def __str__(self):
        return self.nombre


class Eventos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True,max_length=100,verbose_name='Nombre')
    descripcion = models.TextField(blank=True)
    fechayhora = models.DateTimeField(null=False,verbose_name='Fecha y Hora')
    direccion = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to="projects",verbose_name="Imagen")
    asistentes = models.ManyToManyField(settings.AUTH_USER_MODEL,through='Asistente')
    
    class Meta:
        verbose_name="Evento"
        verbose_name_plural="Eventos"

    def __str__(self):
        return self.nombre

class Calendario(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 200, null = True, blank = True)
    fechayhora = models.DateTimeField(null = True, blank = True)

    class Meta:
        db_table = "tb_calendar"

@receiver(post_save, sender = Eventos)
def datos_eventos(sender, instance, created, **kwargs):
    if created:
        Calendario.objects.create(nombre = instance.nombre, fechayhora = instance.fechayhora)

@receiver(post_delete, sender = Eventos)
def eliminado_eventos(sender, instance, **kwargs):
    Calendario.objects.filter(nombre = instance.nombre).delete()

@receiver(post_save, sender = Eventos)
def actualizar_eventos(sender, instance, created, **kwargs):
    eventos = Calendario.objects.filter(nombre = instance.nombre).first()
    if eventos:
        eventos.nombre = instance.nombre
        eventos.fechayhora = instance.fechayhora
        eventos.save()

class Asistente(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evento = models.ForeignKey(Eventos, on_delete=models.CASCADE)


class Actividad(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='Usuario',on_delete=models.CASCADE)
    verb = models.CharField(max_length=200)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True,
    related_name='target_obj', on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.pk 
  
class Cursos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True,max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.IntegerField(blank=False,null=False)
    archivo = models.FileField(upload_to="uploads",verbose_name="archivo")

    class Meta:
        verbose_name="Curso"
        verbose_name_plural="Cursos"

    def __str__(self):
        return self.nombre

class Mensaje(models.Model):
    id = models.AutoField(primary_key=True)
    remitente = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField(blank=False)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name="Mensaje"
        verbose_name_plural="Mensajes"