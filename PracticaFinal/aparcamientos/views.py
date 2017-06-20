from django.shortcuts import render
from aparcamientos.models import Aparcamiento, Cambio, Comentario, Elegido
from aparcamientos.parsear import parsear_fichero
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.db.models import Count
import xml.etree.ElementTree as ET
from django.db.models import Count
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
                #elif "ORIENTACION" in elem.attrib.values():
                #    aparcamiento_nuevo.orientacion = elem.text
                #elif "LOCALIDAD" in elem.attrib.values():
                #    aparcamiento_nuevo.localidad = elem.text
                #elif "PROVINCIA" in elem.attrib.values():
                #    aparcamiento_nuevo.provincia = elem.text
                #elif "CODIGO-POSTAL" in elem.attrib.values():
                #    aparcamiento_nuevo.codigoPostal = elem.text
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
    #lista_cambios = Cambio.objects.all()
    #lista_usuarios = User.objects.all()
    #if len(lista_cambios) != len(lista_usuarios):
    #    for usuario in lista_usuarios:
    #        try:
    #            user = Cambio.objects.get(usuario=usuario)
    #        except Cambio.DoesNotExist:
    #            user = Cambio(usuario=usuario)
    #            user.save()

    #    lista_cambios = Cambio.objects.all()

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
    # Obtener todos los valores de la BD para un campo del modelo:
    # http://stackoverflow.com/questions/6653382/python-django-load-column-from-database-into-list
    lista_distritos = Aparcamiento.objects.all().values_list('distrito')

    # Obtener los valores únicos de una lista:
    # http://stackoverflow.com/questions/12897374/get-unique-values-from-a-list-in-python
    lista_distritos_unicos = list(set(lista_distritos))

    # Convertir lista de tuplas en lista:
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

def pag_aparcamiento(request, idEntidad):
    aparcamiento = Aparcamiento.objects.get(idEntidad = idEntidad)
    nombre = aparcamiento.nombre
    comentarios = Comentario.objects.filter(aparcamiento = aparcamiento)
    if len(comentarios) != 0:
        Comentarios_vacio = False;
    else:
        Comentarios_vacio = True;
    try:
        coment_usu = Comentario.objects.get(aparcamiento = aparcamiento, usuario = request.user.username)
        NoComent = False
    except Comentario.DoesNotExist:
        NoComent = True
    lista_comentarios=[]
    for coment in comentarios:
        lista_comentarios.append((coment.usuario, coment.texto, coment.fecha))

    #visitas = contador_visitas(identificador)
    #megustas = contador_megustas(identificador)
    template = get_template('pag_aparcamiento.html')
    #context = RequestContext(request, {'aparcamiento': aparcamiento,'comentarios': lista_comentarios, 'NoComent': NoComent, 'Comentarios_vacio': Comentarios_vacio, 'visitas': visitas, 'megustas': megustas})
    context = RequestContext(request, {'aparcamiento': aparcamiento,'comentarios': lista_comentarios, 'NoComent': NoComent, 'Comentarios_vacio': Comentarios_vacio})
    resp = template.render(context)
    return HttpResponse(resp)

def pag_usuario(request, usu):
    if request.method == "GET":
        try:
            usuario = User.objects.get(username=usu)
        except User.DoesNotExist:
            template = get_template('error.html')
            return HttpResponse(template.render(), status=404)

        # Como obtener una query string:
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
        # Como extraer entradas utilizando los operadores de desigualdad:
        # http://stackoverflow.com/questions/10040143/how-to-do-a-less-than-or-equal-to-filter-in-django-queryset
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

        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            # Correct password, and the user is marked "active"
            if usuario.is_active:
                login(request, usuario)
    # Redirect to a success page.
    return HttpResponseRedirect('/')


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















#A PARTIR DE AQUI NO VALE NADA DE MOMENTO

# guarda los datos del xml en la base de datos
def cargar_bd(request):

    datos = parsear_fichero('http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full')
    #datos va a ser una lista de diccionarios(ver parsear_fichero)
    for aparcamiento in datos: # aparcamiento es un diccionario
        try:
            nuevo_aparc = Aparcamiento(nombre = aparcamiento["NOMBRE"],contentUrl = aparcamiento["CONTENT-URL"],
                    descripcion = aparcamiento["DESCRIPCION"], barrio = aparcamiento["BARRIO"],
                    distrito = aparcamiento["DISTRITO"], accesibilidad= aparcamiento["ACCESIBILIDAD"],
                    latitud = aparcamiento["LATITUD"],longitud = aparcamiento["LONGITUD"])
        except KeyError:
            continue
        nuevo_aparc.save()
        #id_entidad = aparcamiento.get('ID-ENTIDAD')
        #nombre = aparcamiento.get('NOMBRE')
        #url = aparcamiento.get('CONTENT-URL')
        #descripcion = aparcamiento.get('DESCRIPCION')
        #nombre_via = aparcamiento.get('NOMBRE-VIA')
        #clase_vial = aparcamiento.get('CLASE-VIAL')
        #tipo_numero = aparcamiento.get('TIPO-NUMERO')
        #numero = aparcamiento.get('NUM')
        #barrio = aparcamiento.get('BARRIO')
        #distrito = aparcamiento.get('DISTRITO')
        #latitud = aparcamiento.get('LATITUD')
        #longitud = aparcamiento.get('LONGITUD')

        #accesibilidad = aparcamiento.get('ACCESIBILIDAD')
        #telefono = aparcamiento.get('TELEFONO')
        #email = aparcamiento.get('EMAIL')

        #creamos el nuevo aparcamiento con los datos obtenidos y lo guardamos
        #nuevo_aparc = Aparcamiento(nombre = nombre,contentUrl = url,
        #                        nombreVia = nombre_via, claseVial = clase_vial, tipoNum = tipo_numero,
        #                        num = numero, descripcion = descripcion, latitud = latitud,
        #                        longitud = longitud ,  barrio = barrio, distrito = distrito,
        #                        accesibilidad = accesibilidad, telefono = telefono, email = email)



def cargar_datos(request):
    if request.method == 'GET':
        cargar_bd(request)
        try:
            lista_usuarios = User.objects.all()
        except:
            lista_usuarios = []
        #lista_aparcamientos = ordenar_comentarios()
        masComentados = Aparcamiento.objects.annotate(
                        num_com=Count('comentario')).order_by('-num_com')[:5]
        accesibilidad = False
        return HttpResponseRedirect("/")

def ordenar_comentarios():

    aparcamientos_comentados = []
    aparcamientos_populares = Aparcamiento.objects.annotate(quantity=Count('comentario')).order_by('-quantity')
    if aparcamientos_populares[0].quantity > 0:
        for i in range(5):
            if aparcamientos_populares[i].quantity > 0:
                aparca = aparcamiento.objects.get(nombre=aparcamientos_populares[i])
                aparcamientos_comentados += {aparca}

    return aparcamientos_comentados

    #aparcamientos = Aparcamiento.objects.all()
    #dicc_aparcamiento_coment = {}
    #for aparcamiento in aparcamientos:
    #    if aparcamiento.comentarios_set.count() != 0:
    #        dicc_aparcamiento_coment[aparcamiento.nombre] = aparcamiento.comentarios_set.count()
          # cuenta los comentarios que hay y los guardo en un diccionario
            # siendo el aparcamiento la clave y el valor el numero de comentarios
    #if len(dicc_aparcamiento_coment) != 0:
    #    list_aparca_coment = dicc_hotel_coment.items() #lo tengo que pasar a lista para poder ordenarlo
    #    list_aparca_coment.sort(key=lambda x: x[1], reverse=True)
    #    if len(list_aparca_coment) >= 5:
    #        list_aparca_coment = list_aparca_coment[:10]
    #else:
    #    list_aparca_coment = []

    #return list_aparca_coment

#def pag_principal(request):
#    lista_aparcamientos = Aparcamiento.objects.all()
#    accesibilidad = ''
#    if not lista_aparcamientos:
#        lista_aparcamientos = parsear_fichero('http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full')
#        for aparcamiento in lista_aparcamientos: # aparcamiento es un diccionario
#            try:
#                nuevo_aparc = Aparcamiento(nombre = aparcamiento["NOMBRE"],contentUrl = aparcamiento["CONTENT-URL"],
#                descripcion = aparcamiento["DESCRIPCION"], barrio = aparcamiento["BARRIO"],
#                distrito = aparcamiento["DISTRITO"], accesibilidad= aparcamiento["ACCESIBILIDAD"],latitud = aparcamiento["LATITUD"],
#                longitud = aparcamiento["LONGITUD"], telefono= aparcamiento["TELEFONO"], email= aparcamiento["EMAIL"])
#            except:
#                try:
#                    nuevo_aparc = Aparcamiento(nombre = aparcamiento["NOMBRE"],contentUrl = aparcamiento["CONTENT-URL"],
##                    descripcion = aparcamiento["DESCRIPCION"], barrio = aparcamiento["BARRIO"],
#                    distrito = aparcamiento["DISTRITO"], accesibilidad= aparcamiento["ACCESIBILIDAD"],latitud = aparcamiento["LATITUD"],
#                    longitud = aparcamiento["LONGITUD"]) #hay algunos que no tienen telefono ni email
#                except:
#                    try:
#                        nuevo_aparc = Aparcamiento(nombre = aparcamiento["NOMBRE"],contentUrl = aparcamiento["CONTENT-URL"],
#                        descripcion = aparcamiento["DESCRIPCION"], barrio = aparcamiento["BARRIO"],
#                        distrito = aparcamiento["DISTRITO"], accesibilidad= aparcamiento["ACCESIBILIDAD"])
#                    except:
#                        continue


#            nuevo_aparc.save()
    #ordenamos por comentarios
#    aparcamientos_comentados = ordenar_comentarios()
    #aparcamientos_comentados = []
    #aparcamientos_populares = Aparcamiento.objects.annotate(quantity=Count('comentario')).order_by('-quantity')
    #if aparcamientos_populares[0].quantity > 0:
    #    for i in range(5):
    #        if aparcamientos_populares[i].quantity > 0:
    #            aparca = aparcamiento.objects.get(nombre=aparcamientos_populares[i])
    #            aparcamientos_comentados += {aparca}
    #CONSTRUYE LISTA DE URL's DE USERS
    #user_list = []
    #users = User.objects.all()
    #for user in users:
    #    if str(user) != "superuser":
    #        config = CSS.objects.get(user=user)
    #        user_list += [(user, config.title)]
#    lista_usuarios = User.objects.all()
#    lista_titulos = []
#    for usu in lista_usuarios:
#        try:
#            cambio = Cambios.objects.get(usuario=usu.username)
#            if cambio.titulo != '':
#                titulo = cambio.titulo
#            else:
#                titulo = "Pagina de " + usu.username
#                lista_titulos.append((titulo, usu.username))
#        except:
#            titulo = "Pagina de " + usu.username
#            lista_titulos.append((titulo, usu.username))

    #cargamos el html
#    template = get_template('pag_ppal.html')
#    context = RequestContext(request, {'aparcamientos_populares' : aparcamientos_comentados, 'lista_titulos': lista_titulos, 'accesibilidad': accesibilidad})
        #context = RequestContext(request, {'lista_aparcamientos':  'lista_titulos'})
#    resp = template.render(context)
#    return HttpResponse(resp)

def about(request):
    template = get_template('about.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def poner_espacios(frase_inicial):
    palabras = frase_inicial.split('+')
    frase = ''
    for palabra in palabras:

        frase += palabra + ' '
    return frase

@csrf_exempt
def poner_comentario(request, identificador):
    if request.method == 'POST':
        usuario = request.user.username
        aparca = Aparcamiento.objects.get(id=int(identificador))
        comentario = request.body.split('&')[0].split('=')[1] #el primer 1 depende de lo que imprima el request.body pq a veces el primer campo es algo que pone el navegador
        comentario = poner_espacios(comentario)
        nuevo_comentario = Comentario(aparcamiento=aparca, texto=comentario, usuario=usuario)
        nuevo_comentario.save()
        direccion = "/aparcamientos/" + str(identificador)
        return HttpResponseRedirect(direccion)
    else:
        return HttpResponse("Error")



def anadir_aparcamiento_pag(request, identificador):
    try:
        aparca = Aparcamiento.objects.get(id=int(identificador))
    except ObjectDoesNotExist:
        template = get_template('error.html')
        return HttpResponse(template.render(Context({'texto': "Lo sentimos, no existe un aparcamiento con dicho identificador"})))
    usuario = request.user.username
    aparcamiento_anadido = Seleccionado(aparcamiento=aparca, usuario=usuario)
    aparcamiento_anadido.save()

    direccion = '/' + usuario
    return HttpResponseRedirect(direccion)



#def pag_xml(request):
#    lista_nombres_aparcamientos = ordenar_comentarios()
#    if len(lista_nombres_aparcamientos) == 0:
#        vacio = True
#    else:
#        vacio = False
#    lista_aparcamientos = []
#    for nombre in lista_nombres_aparcamientos:
#        aparcamiento = Aparcamiento.objects.get(nombre = nombre[0])
#        lista_aparcamientos.append((hotel))
#    template = get_template('pag_ppal.xml')
#    context = RequestContext(request, {'lista_aparcamientos': lista_aparcamientos, 'vacio': vacio})
#    return HttpResponse(template.render(context), content_type="text/xml")

def css(request):
    usuario = request.user.username
    letra_defecto = '1.3em'
    color_defecto = 'white'
    titulo_defecto = "Pagina de " + request.user.username

    if request.method == "POST":

        color = request.body.split('&')[1].split('=')[1]
        letra = request.body.split('&')[2].split('=')[1]

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
                color = su_cambio.color
                letra = su_cambio.letra
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
        titulo = request.body.split('&')[1].split('=')[1]
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

#def cargar_bd(request):
    # No fui capaz de parsear con lo de barrapunto y encontré esto
    # http://stackoverflow.com/questions/2792650/python3-error-import-error-no-module-name-urllib2
#    xmlFile = urlopen("http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full")
#    arbol = ET.parse(xmlFile)
#    raiz = arbol.getroot()

#    for elemento in arbol.iter():
#        aparcamiento_nuevo = ''
#        if "ID-ENTIDAD" in elemento.attrib.values():   # Es un diccionario
#            aparcamiento_nuevo = Aparcamiento(idEntidad=elemento.text)
#        elif "NOMBRE" in elemento.attrib.values():
#            aparcamiento_nuevo.nombre = elemento.text
#        elif "CONTENT-URL" in elemento.attrib.values():
#            aparcamiento_nuevo.contentUrl = elemento.text
#        elif "NOMBRE-VIA" in elemento.attrib.values():
#            aparcamiento_nuevo.nombreVia = elemento.text
#        elif "CLASE-VIAL" in elemento.attrib.values():
#            aparcamiento_nuevo.claseVial = elemento.text
#        elif "TIPO-NUM" in elemento.attrib.values():
#            aparcamiento_nuevo.tipoNum = elemento.text
#        elif "NUM" in elemento.attrib.values():
#            aparcamiento_nuevo.num = elemento.text
#        elif "DESCRIPCION" in elemento.attrib.values():
#            aparcamiento_nuevo.descripcion = elemento.text


        #elif "ORIENTACION" in elemento.attrib.values():
        #    aparcamiento_nuevo.orientacion = elemento.text
        #elif "LOCALIDAD" in elemento.attrib.values():
        #    aparcamiento_nuevo.localidad = elemento.text
        #elif "PROVINCIA" in elemento.attrib.values():
        #    aparcamiento_nuevo.provincia = elemento.text
        #elif "CODIGO-POSTAL" in elemento.attrib.values():
        #    aparcamiento_nuevo.codigoPostal = elemento.text
#       elif "LATITUD" in elemento.attrib.values():
#            aparcamiento_nuevo.latitud = elemento.text
#        elif "LONGITUD" in elemento.attrib.values():
#            aparcamiento_nuevo.longitud = elemento.text
#        elif "BARRIO" in elemento.attrib.values():
#            aparcamiento_nuevo.barrio = elemento.text
#        elif "DISTRITO" in elemento.attrib.values():
#            aparcamiento_nuevo.distrito = elemento.text
#        elif "ACCESIBILIDAD" in elemento.attrib.values():
#            aparcamiento_nuevo.accesibilidad = elemento.text
        #elif "COORDENADA-X" in elemento.attrib.values():
        #    aparcamiento_nuevo.coordenadaX = elemento.text
        #elif "COORDENADA-Y" in elemento.attrib.values():
        #    aparcamiento_nuevo.coordenadaY = elemento.text

#        elif "TELEFONO" in elemento.attrib.values():
#            aparcamiento_nuevo.telefono = elemento.text
#        elif "EMAIL" in elemento.attrib.values():
#            aparcamiento_nuevo.email = elemento.text
#        elif "TIPO" in elemento.attrib.values():
#            aparcamiento_nuevo.save()
#        else:
#            pass
        #return(aparcamiento_nuevo)

#@csrf_exempt
#def pag_principal(request):
#    template = get_template('pag_ppal.html')
#    if request.method == "POST":
#        if "boton" in request.POST:
#            opcion = request.POST['boton']
#            if opcion == "Activar":
#                mas_comentados = Aparcamiento.objects.annotate(
#                                num_com=Count('comentario')).filter(
#                                accesibilidad=1).order_by('-num_com')[:5] #Tienen que ir de 5 en 5
#                accesibilidad = True
#        else:
#            opcion = ""
            # Parsear en Python3 con ElementTree una URL:
            # http://stackoverflow.com/questions/2792650/python3-error-import-error-no-module-name-urllib2
#            xmlFile = urlopen("http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full")
#            arbol = ET.parse(xmlFile)
#            raiz = arbol.getroot()

#            for elem in arbol.iter():
#                if "ID-ENTIDAD" in elem.attrib.values():   # Es un diccionario
#                    nuevoAparcamiento = Aparcamiento(idEntidad=elem.text)
#                elif "NOMBRE" in elem.attrib.values():
#                    nuevoAparcamiento.nombre = elem.text
#                elif "DESCRIPCION" in elem.attrib.values():
#                    nuevoAparcamiento.descripcion = elem.text
#                elif "ACCESIBILIDAD" in elem.attrib.values():
#                    nuevoAparcamiento.accesibilidad = elem.text
#                elif "CONTENT-URL" in elem.attrib.values():
#                    nuevoAparcamiento.contentUrl = elem.text
#                elif "NOMBRE-VIA" in elem.attrib.values():
#                    nuevoAparcamiento.nombreVia = elem.text
#                elif "CLASE-VIAL" in elem.attrib.values():
#                    nuevoAparcamiento.claseVial = elem.text
#                elif "TIPO-NUM" in elem.attrib.values():
#                    nuevoAparcamiento.tipoNum = elem.text
#                elif "NUM" in elem.attrib.values():
#                    nuevoAparcamiento.num = elem.text
#                elif "ORIENTACION" in elem.attrib.values():
#                    nuevoAparcamiento.orientacion = elem.text
#                elif "LOCALIDAD" in elem.attrib.values():
#                    nuevoAparcamiento.localidad = elem.text
#                elif "PROVINCIA" in elem.attrib.values():
#                    nuevoAparcamiento.provincia = elem.text
#                elif "CODIGO-POSTAL" in elem.attrib.values():
#                    nuevoAparcamiento.codigoPostal = elem.text
#                elif "BARRIO" in elem.attrib.values():
#                    nuevoAparcamiento.barrio = elem.text
#                elif "DISTRITO" in elem.attrib.values():
#                    nuevoAparcamiento.distrito = elem.text
#                elif "COORDENADA-X" in elem.attrib.values():
#                    nuevoAparcamiento.coordenadaX = elem.text
#                elif "COORDENADA-Y" in elem.attrib.values():
#                    nuevoAparcamiento.coordenadaY = elem.text
#                elif "LATITUD" in elem.attrib.values():
#                    nuevoAparcamiento.latitud = elem.text
#                elif "LONGITUD" in elem.attrib.values():
#                    nuevoAparcamiento.longitud = elem.text
#                elif "TELEFONO" in elem.attrib.values():
#                    nuevoAparcamiento.telefono = elem.text
#                elif "EMAIL" in elem.attrib.values():
#                    nuevoAparcamiento.email = elem.text
#                elif "TIPO" in elem.attrib.values():
#                    nuevoAparcamiento.save()
#                else:
#                    pass

#    if request.method == "GET" or opcion == "Desactivar" or opcion == "":
        # Agrupar los aparcamientos por los 5 más comentados:
        # https://docs.djangoproject.com/en/1.8/topics/db/aggregation/
#        masComentados = Aparcamiento.objects.annotate(
#                        num_com=Count('comentario')).order_by('-num_com')[:5]
#        accesibilidad = False

#    listaPreferencias = Cambio.objects.all()
#    listaUsuarios = User.objects.all()
#    if len(listaPreferencias) != len(listaUsuarios):
#        for usuario in listaUsuarios:
#            try:
#                user = Cambio.objects.get(usuario=usuario)
#            except Cambio.DoesNotExist:
#                user = Cambio(usuario=usuario)
#                user.save()

#        listaPreferencias = Cambio.objects.all()

#    listaAparcamientos = Aparcamiento.objects.all()
#    if len(listaAparcamientos) == 0:
#        cargar = True
#    else:
#        cargar = False

    # Renderizar correctamente todo el contexto (el login y las variables):
    # https://docs.djangoproject.com/en/1.8/ref/templates/api/#playing-with-context-objects
#    contexto = RequestContext(request, {'listaUsuarios': listaPreferencias,
#                                        'accesibilidad': accesibilidad,
#                                        'masComentados': masComentados,
#                                        'cargar': cargar})

#    return HttpResponse(template.render(contexto))
