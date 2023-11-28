from django.contrib import admin
from .models import Eventos,Cursos,Actividad,Mensaje,Asistente, UserProfile
# Register your models here.

class UserDetail(admin.ModelAdmin):
    list_display = ("nombre","correo","register_date")
    fields = ["nombre","correo","password","register_date"]
    readonly_fields = ('register_date', )
    search_fields = ("nombre", )


class AsistenteInline(admin.TabularInline):
    model = Asistente
    extra = 1

class EventoDet(admin.ModelAdmin):
    inlines = [AsistenteInline, ]
    list_display = ("nombre","fechayhora","direccion")
    search_fields = ("nombre", )
    fields = ["nombre","descripcion","fechayhora","direccion","imagen"]


class CursoDet(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre", )
    fields = ["nombre","descripcion", "precio","archivo"]

class MensajeDet(admin.ModelAdmin):
    readonly_fields = ('creado', )

admin.site.register(Eventos,EventoDet)
admin.site.register(Cursos,CursoDet)
admin.site.register(Actividad)
admin.site.register(Mensaje,MensajeDet)
admin.site.register(UserProfile,UserDetail)
