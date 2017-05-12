from django.db import models

# Create your models here.
class Aparcamiento(models.Model):
    nombre = models.CharField(max_length=32)
    direccion = models.CharField(max_length=300)
    descripcion = models.TextField()
    #latitud
    #longitud
    #barrio
    #distrito
    #contacto

class Comentarios(models.Model):
    aparcamiento = models.ForeignKey(Aparcamiento)
    texto = models.TextField()
    usuario = models.CharField(max_length=32)

class Elegidos(models.Model):
    aparcamiento = models.ForeignKey(Aparcamiento)
    usuario = models.CharField(max_length=32)
    #fecha?

class Cambios(models.Model): #cambiar el estilo CSS
    usuario = models.CharField(max_length=32)
    letra = models.CharField(max_length=32)
    color = models.CharField(max_length=32)
    #titulo = models.CharField(max_length=64, default='')

#aparcamientos accesibles?
