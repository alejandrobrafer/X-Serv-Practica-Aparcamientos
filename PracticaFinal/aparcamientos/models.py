from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Aparcamiento(models.Model):
    idEntidad = models.IntegerField()
    nombre = models.CharField(max_length=32)
    contentUrl = models.URLField(max_length=300)
    descripcion = models.TextField()
    barrio = models.CharField(max_length=32)
    distrito = models.CharField(max_length=32)
    nombreVia = models.CharField(max_length=64)
    claseVial = models.CharField(max_length=32)
    tipoNum = models.CharField(max_length=32, blank=True)
    num = models.CharField(max_length=32, blank=True)
    accesibilidad = models.IntegerField(choices=((0, '0'), (1, '1')))
    coordenadaX = models.PositiveIntegerField()
    coordenadaY = models.PositiveIntegerField()
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    telefono = models.TextField()
    email = models.TextField()

class Comentario(models.Model):
    aparcamiento = models.ForeignKey(Aparcamiento)
    texto = models.TextField()

class Cambio(models.Model):
    usuario = models.CharField(max_length=32)
    titulo = models.CharField(max_length=64, default='')
    letra = models.CharField(max_length=64, null=True, blank=True)
    color = models.CharField(max_length=32)


class Elegido(models.Model):
    aparcamiento = models.ForeignKey(Aparcamiento)
    usuario = models.CharField(max_length=32)
    fecha = models.DateField(auto_now = True)

class Megusta(models.Model):
    aparcamiento = models.ForeignKey(Aparcamiento)
    usuario = models.CharField(max_length=32)
