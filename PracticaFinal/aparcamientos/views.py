from django.shortcuts import render
from aparcamientos.models import Aparcamiento, Cambio, Comentario, Elegido, Megusta
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.db.models import Count
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from django.utils import timezone
# Create your views here.

@csrf_exempt
def pag_principal(request):
    accesibilidad = True
    aparcamientos_comentados = ''
    if request.method == "POST":
        if "boton" in request.POST:
            opcion = request.POST['boton']
            if opcion == "Activar":
                aparcamientos_comentados = Aparcamiento.objects.annotate(
                                num_com=Count('comentario')).filter(
                                accesibilidad=1).order_by('-num_com')[:5]
                accesibilidad = True
        else:
            opcion = ""
            #Para parsear no lo conseguí lograr con el parsea de barrapunto y encontré esto:
            # http://stackoverflow.com/questions/2792650/python3-error-import-error-no-module-name-urllib2
            xmlFile = urlopen("http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full")
            arbol = ET.parse(xmlFile)
            raiz = arbol.getroot()

            for elem in arbol.iter():
                if "ID-ENTIDAD" in elem.attrib.values():   # Es un diccionario
                    aparcamiento_nuevo = Aparcamiento(idEntidad=elem.text)
                elif "NOMBRE" in elem.attrib.values():
                    aparcamiento_nuevo.nombre = elem.text
                elif "CONTENT-URL" in elem.attrib.values():
                    aparcamiento_nuevo.contentUrl = elem.text
                elif "DESCRIPCION" in elem.attrib.values():
                    aparcamiento_nuevo.descripcion = elem.text
                elif "BARRIO" in elem.attrib.values():
                    aparcamiento_nuevo.barrio = elem.text
                elif "DISTRITO" in elem.attrib.values():
                    aparcamiento_nuevo.distrito = elem.text
                elif "NOMBRE-VIA" in elem.attrib.values():
                    aparcamiento_nuevo.nombreVia = elem.text
                elif "CLASE-VIAL" in elem.attrib.values():
                    aparcamiento_nuevo.claseVial = elem.text
                elif "TIPO-NUM" in elem.attrib.values():
                    aparcamiento_nuevo.tipoNum = elem.text
                elif "NUM" in elem.attrib.values():
                    aparcamiento_nuevo.num = elem.text
                elif "ACCESIBILIDAD" in elem.attrib.values():
                    aparcamiento_nuevo.accesibilidad = elem.text
                elif "COORDENADA-X" in elem.attrib.values():
                    aparcamiento_nuevo.coordenadaX = elem.text
                elif "COORDENADA-Y" in elem.attrib.values():
                    aparcamiento_nuevo.coordenadaY = elem.text
                elif "LATITUD" in elem.attrib.values():
                    aparcamiento_nuevo.latitud = elem.text
                elif "LONGITUD" in elem.attrib.values():
                    aparcamiento_nuevo.longitud = elem.text
                elif "TELEFONO" in elem.attrib.values():
                    aparcamiento_nuevo.telefono = elem.text
                elif "EMAIL" in elem.attrib.values():
                    aparcamiento_nuevo.email = elem.text
                elif "TIPO" in elem.attrib.values():
                    aparcamiento_nuevo.save()
                else:
                    pass
    elif request.method == "GET" or opcion == "Desactivar" or opcion == "":

        aparcamientos_comentados = Aparcamiento.objects.annotate(
                        num_com=Count('comentario')).order_by('-num_com')[:5]
        accesibilidad = False

    try:
        lista_usuarios = User.objects.all()
        lista_titulos = []
        for usu in lista_usuarios:
            try:
                mod = Cambio.objects.get(usuario=usu.username)
                if mod.titulo != '':
                    titulo = mod.titulo
                else:
                    titulo = "Pagina de " + usu.username
                lista_titulos.append((titulo, usu.username))
            except:
                titulo = "Pagina de " + usu.username
                lista_titulos.append((titulo, usu.username))
    except:
        lista_usuarios = []

    lista_aparcamientos = Aparcamiento.objects.all()
    if len(lista_aparcamientos) == 0:
        cargar = True
    else:
        cargar = False

    template = get_template('pag_ppal.html')
    context = RequestContext(request, {'lista_titulos': lista_titulos,
                                        'accesibilidad': accesibilidad,
                                        'aparcamientos_comentados': aparcamientos_comentados,
                                        'cargar': cargar})

    resp = template.render(context)
    return HttpResponse(resp)

@csrf_exempt
def pag_aparcamientos(request):
    lista_aparcamientos = ''
    distrito = ''
    if request.method == 'POST':
        if "opciones" in request.POST:
            distrito = request.POST['opciones']
            if distrito == "Todos":
                lista_aparcamientos = Aparcamiento.objects.all()
            else:
                lista_aparcamientos = Aparcamiento.objects.filter(
                                     distrito=distrito)
        else:
            if "marcar" in request.POST:
                recibido = request.POST['marcar']
                idEntidad = recibido.split(',')[0]
                name_usuario = recibido.split(',')[1]
                aparcamiento = Aparcamiento.objects.get(idEntidad=idEntidad)
                usuario = User.objects.get(username=name_usuario)
                fecha = timezone.now()
                nueva_eleccion = Elegido(aparcamiento=aparcamiento,
                                            usuario=usuario,
                                            fecha=fecha)
                nueva_eleccion.save()
            else:
                recibido = request.POST['desmarcar']
                idEntidad = recibido.split(',')[0]
                name_usuario = recibido.split(',')[1]
                aparcamiento = Aparcamiento.objects.get(idEntidad=idEntidad)
                usuario = User.objects.get(username=name_usuario)
                borrar_eleccion = Elegido.objects.get(
                                  aparcamiento=aparcamiento, usuario=usuario)
                borrar_eleccion.delete()

    if request.method == 'GET':
        aparcamientos = Aparcamiento.objects.all()
        distrito = "Todos"
    # Obtengo todos los valores de distrito
    lista_distritos = Aparcamiento.objects.all().values_list('distrito')
    # Obtengo los valores unicos de una lista
    # http://stackoverflow.com/questions/12897374/get-unique-values-from-a-list-in-python
    lista_distritos_unicos = list(set(lista_distritos))
    # http://stackoverflow.com/questions/10941229/convert-list-of-tuples-to-list
    lista_distritos_unicos = [distrito[0] for distrito in lista_distritos_unicos]

    if request.user.is_authenticated():
        elegidos = Elegido.objects.all().values_list(
                        'aparcamiento').filter(usuario=request.user)
        lista_elegidos = [elegido[0] for elegido
                              in elegidos]
    else:
        lista_elegidos = ""

    template = get_template('pagina_aparcamientos.html')
    context = RequestContext(request, {'lista_distritos': lista_distritos_unicos,
                                        'aparcamientos': lista_aparcamientos,
                                        'distrito': distrito,
                                        'elegidos': lista_elegidos})
    return HttpResponse(template.render(context))

@csrf_exempt
def pag_aparcamiento(request, idEntidad):
    if request.method == "GET":
        try:
            aparcamiento = Aparcamiento.objects.get(idEntidad=idEntidad)

        except Aparcamiento.DoesNotExist:
            template = get_template('error.html')
            return HttpResponse(plantilla.render(), status=404)
    else:
        comentario = request.POST['texto']
        aparcamiento = Aparcamiento.objects.get(idEntidad=idEntidad)
        nuevoComentario = Comentario(aparcamiento=aparcamiento,texto=comentario)
        nuevoComentario.save()

    visitas = contador_visitas(idEntidad)
    megustas = contador_megustas(idEntidad)
    template = get_template('pag_aparcamiento.html')
    comentarios = Comentario.objects.filter(aparcamiento=aparcamiento)
    context = RequestContext(request, {'aparcamiento': aparcamiento,
                              'comentarios': comentarios,
                              'megustas': megustas,
                              'visitas':visitas})

    resp = template.render(context)
    return HttpResponse(resp)

def pag_usuario(request, usu):
    if request.method == "GET":
        try:
            usuario = User.objects.get(username=usu)
        except User.DoesNotExist:
            template = get_template('error.html')
            return HttpResponse(template.render(), status=404)
        # Obtener una query string:
        # https://docs.djangoproject.com/en/1.8/ref/request-response/#django.http.HttpRequest.META
        qs = request.META['QUERY_STRING']
    else:
        qs = ""
        if request.user.is_authenticated():
            usuario = User.objects.get(username=request.user.username)
            try:
                usuario = Cambio.objects.get(usuario=usuario)
            except:
                user = User.objects.get(username=request.user.username)
                usuario = Cambio(usuario=user)

            if 'titulo' in request.POST:
                usuario.titulo = request.POST['titulo']
            else:
                usuario.letra = request.POST['letra']
                usuario.color = request.POST['color']
            usuario.save()

    template = get_template('pag_usuario.html')
    usuario = User.objects.get(username=usu)
    if qs == "":
        elegidos = Elegido.objects.filter(usuario=usuario)
    else:
        restantes = Elegido.objects.filter(id__gt=(int(qs)))
        elegidos = restantes.filter(usuario=usuario)

    if len(elegidos) <= 5:
        fin = True
    else:
        fin = False

    try:
        usuario = Cambio.objects.get(usuario=usuario)
    except:
        usuario = ""

    context = RequestContext(request, {'usuario': usuario,
                                        'usu': usu,
                                        'elegidos': elegidos,
                                        'fin': fin})
    resp = template.render(context)
    return HttpResponse(resp)

@csrf_exempt
def login(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        template = get_template('error.html')
        return HttpResponse(template.render(Context({'texto': "Usuario no autenticado"})))


@csrf_exempt
def logout(request):
    if request.method == "POST":
        logout(request)
    return HttpResponseRedirect('/')

def pag_xml(request, usu):
    try:
        usuario = User.objects.get(username=usu)
    except User.DoesNotExist:
        template = get_template('error.html')

        return HttpResponse(template.render(), status=404)

    template = get_template('canal_usuario.xml')
    elegidos = Elegido.objects.filter(usuario=usuario)
    context = RequestContext(request, {'usuario': usuario,'elegidos': elegidos})
    resp = template.render(context)

    return HttpResponse(resp, content_type="text/xml")

def css(request):

    usuario = request.user.username
    letra_defecto = '14px'
    color_defecto = '##00FF00'
    titulo_defecto = "Pagina de " + usuario

    if request.method == "POST":
        color = request.POST['color']
        letra = request.POST['letra']
        if color != "PorDefecto" and letra != "PorDefecto":

            try:
                cambio = Cambio.objects.get(usuario=usuario)
                cambio.color = color
                cambio.letra = letra
                cambio.save()
            except:
                cambio = Cambio(usuario=usuario, titulo=titulo_defecto, letra=letra, color=color)
                cambio.save()
        elif color != "PorDefecto" and letra == "PorDefecto":
            try:
                cambio = Cambio.objects.get(usuario=usuario)
                cambio.color = color
                cambio.letra = letra_defecto
                cambio.save()
            except:
                cambio = Cambio(usuario=usuario, titulo=titulo_defecto, letra=letra_defecto, color=color)
                cambio.save()
        elif color == "PorDefecto" and letra != "PorDefecto":
            try:
                cambio = Cambio.objects.get(usuario=usuario)
                cambio.color = color_defecto
                cambio.letra = letra
                cambio.save()
            except:
                cambio = Cambio(usuario=usuario, titulo=titulo_defecto, letra=letra, color=color_defecto)
                cambio.save()
        elif color == "PorDefecto" and letra == "PorDefecto":
            try:
                cambio = Cambio.objects.get(usuario=usuario)
                cambio.color = color_defecto
                cambio.letra = letra_defecto
                cambio.save()
            except:
                cambio = Cambio(usuario=usuario, titulo=titulo_defecto, letra=letra_defecto, color=color_defecto)
                cambio.save()

        direccion = '/' + usuario
        return HttpResponseRedirect(direccion)
    elif request.method == "GET":
        color = "yellow"
        if request.user.is_authenticated:
            try:
                cambio_suyo = Cambio.objects.get(usuario=usuario)
                color = cambio_suyo.color
                letra = cambio_suyo.letra
            except:
                color = color_defecto
                letra = letra_defecto
        template = get_template('styles.css')
        context = RequestContext(request, {'color': color, 'letra': letra})
        return HttpResponse(template.render(context), content_type="text/css")



def cambiar_titulo(request):
    letra_defecto = '1.3em'
    color_defecto = 'white'
    if request.method == "POST":
        titulo = request.POST['titulo']
        titulo = poner_espacios(titulo)
        try:
            cambio = Cambio.objects.get(usuario=request.user.username)
            cambio.titulo = titulo
            cambio.save()
        except:
            cambio = Cambio(usuario=request.user.username, titulo=titulo, letra=letra_defecto, color=color_defecto)
            cambio.save()
        direccion = '/' + request.user.username
        return HttpResponseRedirect(direccion)

def poner_espacios(frase_inicial):
    palabras = frase_inicial.split('+')
    frase = ''
    for palabra in palabras:

        frase += palabra + ' '
    return frase


def about(request):
    template = get_template('about.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def anadir_megusta(request, idEntidad):
    usu_id = request.user.id
    if usu_id == None:
        usu_id = request.COOKIES['sessionid']
    aparcamiento = Aparcamiento.objects.get(idEntidad=idEntidad)
    try:
        d = Megusta.objects.get(aparcamiento=aparcamiento, usuario=usu_id)
        #no hay que hacer nada, una misma persona no puede poner mas de un me gusta en un mismo alojamiento
    except:
        like = Megusta(aparcamiento=aparcamiento, usuario=usu_id)
        like.save()

    direccion = '/aparcamientos/' + idEntidad
    return HttpResponseRedirect(direccion)

def contador_megustas(idEntidad):
    try:
        aparcamiento = Aparcamiento.objects.get(idEntidad=idEntidad)
        megustas = aparcamiento.megusta_set.count()
    except:
        megustas = 0
    return megustas

def rss(request):
    comentarios = Comentario.objects.all()
    template = get_template('canal.rss')
    context = RequestContext(request, {'comentarios': comentarios})
    resp = template.render(context)
    return HttpResponse(resp,content_type="text/rss+xml")

def contador_visitas(idEntidad):
    aparcamiento = Aparcamiento.objects.get(idEntidad = idEntidad)
    aparcamiento.visitas += 1
    visitas = aparcamiento.visitas
    aparcamiento.save()
    return visitas

def ranking_visitas(request):
    todos_aparcamientos = Aparcamiento.objects.all()
    lista = []
    for aparcamiento in todos_aparcamientos:
        lista.append((aparcamiento.nombre, aparcamiento.visitas, aparcamiento.idEntidad))

    lista.sort(key=lambda x: x[1], reverse=True)

    template = get_template('visitados.html')
    context = RequestContext(request, {'lista':lista})
    resp = template.render(context)
    return HttpResponse(resp)

def pag_ppal_xml(request, usu):

    try:
        usuario = User.objects.get(username=usu)
    except User.DoesNotExist:
        template = get_template('error.html')

        return HttpResponse(template.render(), status=404)

    template = get_template('canal_usuario.xml')
    elegidos = Elegido.objects.filter(usuario=usuario)
    context = RequestContext(request, {'usuario': usuario,'elegidos': elegidos})
    resp = template.render(context)

    return HttpResponse(resp, content_type="text/xml")

def pag_ppal_xml(request):
    aparcamientos_comentados = Aparcamiento.objects.annotate(
                    num_com=Count('comentario')).order_by('-num_com')[:5]
    template = get_template('pag_ppal.xml')
    context = RequestContext(request, {'aparcamientos_comentados': aparcamientos_comentados})
    resp = template.render(context)
    return HttpResponse(resp, content_type="text/xml")
    #aparcamientos_comentados = Aparcamiento.objects.annotate(
    #                num_com=Count('comentario')).order_by('-num_com')[:5]
    #lista_aparcamientos = []
    #for nombre in aparcamientos_comentados:
    #    aparcamientos = Aparcamiento.objects.filter(nombre=nombre)

    #    lista_aparcamientos.append((aparcamientos))
    #template = get_template('pag_ppal.xml')
    #context = RequestContext(request, {'lista_aparcamientos': lista_aparcamientos,
    #                                    'aparcamientos':aparcamientos})
    #resp = template.render(context)
    #return HttpResponse(resp, content_type="text/xml")
