
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('cursos/', views.cursos, name='cursos'),
    path('eventos/', views.eventos, name='eventos'),
    path('recursos/', views.recursos, name='recursos'),
    path('testimonios/', views.testimonios, name='testimonios'),
    path('galeria/', views.galeria, name='galeria'),
    path('cyp/', views.cyp, name='cyp'),
]
