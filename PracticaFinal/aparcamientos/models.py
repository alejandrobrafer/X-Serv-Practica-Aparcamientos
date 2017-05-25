from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Aparcamiento(models.Model):
    #idEntidad = models.IntegerField()
    nombre = models.CharField(max_length=32)
    contentUrl = models.URLField(max_length=300)
    descripcion = models.TextField()
    barrio = models.CharField(max_length=32)
    distrito = models.CharField(max_length=32)
    #nombreVia = models.CharField(max_length=64)
    #claseVial = models.CharField(max_length=32)
    #tipoNum = models.CharField(max_length=32, blank=True)
    #num = models.CharField(max_length=32, blank=True)
    accesibilidad = models.IntegerField(choices=((0, '0'), (1, '1')))
    latitud = models.FloatField()
    longitud = models.FloatField()
    telefono = models.TextField()
    email = models.TextField()

class Comentario(models.Model):
    aparcamiento = models.ForeignKey(Aparcamiento)
    texto = models.TextField()
    usuario = models.CharField(max_length=32)
    fecha = models.DateField(auto_now = True)

class Cambio(models.Model): #cambiar el estilo CSS de la pagina del usuario
    usuario = models.ForeignKey(User)
    titulo = models.CharField(max_length=64, default='')
    letra = models.IntegerField()
    color = models.CharField(max_length=32)


class Elegido(models.Model):
    aparcamiento = models.ForeignKey(Aparcamiento)
    usuario = models.CharField(max_length=32)
    fecha = models.DateField(auto_now = True)
