


from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from core import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('cursos/', views.cursos, name='cursos'),
    path('eventos/', views.eventos, name='eventos'),
    path('recursos/', views.recursos, name='recursos'),
    path('testimonios/', views.testimonios, name='testimonios'),
    path('galeria/', views.galeria, name='galeria'),
    path('formulario/', views.formulario, name='formulario'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    path('contactoF/', views.contactoF, name='contactoF'),
    #Urls Admin
    path('inbox/', views.inbox, name='inbox'),
    path('activity/', views.activity, name='activity'),
    path('calendar/', views.calendar, name = 'calendar'),
    path('all_calendar/', views.all_calendar, name = 'all_calendar'),
    path('form/',views.enviar_mensaje, name="form"),
    path('responder',views.responder_mensaje,name='responder_mensaje'),
    path('eliminar/',views.eliminar_mensaje,name='eliminar_mensaje'),
    
    path('cyp/', views.cyp, name='cyp'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns +=static(settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT)

admin.site.index_title = "Panel de Control"
admin.site.site_title = "Tu Apoyo Latino"