from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Aparcamiento(models.Model):
    nombre = models.CharField(max_length=32)
    direccion = models.CharField(max_length=300)
    descripcion = models.TextField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    barrio = models.CharField(max_length=32)
    distrito = models.CharField(max_length=32)
    contacto = models.TextField()

class Comentario(models.Model):
    aparcamiento = models.ForeignKey(Aparcamiento)
    texto = models.TextField()

class Cambio(models.Model): #cambiar el estilo CSS de la pagina del usuario
    usuario = models.ForeignKey(User)
    letra = models.IntegerField()
    color = models.CharField(max_length=32)
    titulo = models.CharField(max_length=64, default='')

class Elegido(models.Model):
    aparcamiento = models.ForeignKey(Aparcamiento)
    usuario = models.CharField(max_length=32)
    fecha = models.DateField(auto_now = True)



#aparcamientos accesibles?
