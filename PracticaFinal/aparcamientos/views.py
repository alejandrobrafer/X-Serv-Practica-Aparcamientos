from django.shortcuts import render
from aparcamientos.models import Aparcamiento, Cambio, Comentario, Elegido
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
# Create your views here.

 # guarda los datos del xml en la base de datos
#def cargar_bd(request, identificador):

#    datos = parsear_fichero('http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full')
    #datos va a ser una lista de diccionarios(ver parsear_fichero)
#    for aparcamiento in datos: # aparcamiento es un diccionario
#        nombre = aparcamiento.get('NOMBRE')
#        if aparcamiento.has_key('DESCRIPCION):
#            descripcion = aparcamiento.get('DESCRIPCION')
#        else:
#            descripcion = ''
#        accesibilidad = aparcamiento.get('ACCESIBILIDAD')
#        web = aparcamiento.get('CONTENT-URL')


#        telefono = hotel.get('phone')
#        direccion = hotel.get('address')
#        cod_postal = hotel.get('zipcode')
#        categoria = hotel.get('Categoria')

        #creamos el nuevo aparcamiento con los datos obtenidos y lo guardamos
#        nuevo_aparc = Aparcamiento(nombre = nombre,direccion = direccion,descripcion = descripcion, latitud = , longitud = longitud ,  barrio = barrio, distrito = distrito, contacto = contacto)
#        nuevo_aparc.save()

        #for elemento in hotel.get('url_fotos'):
        #        nombre_hotel = Alojamiento.objects.get(nombre = nombre)
        #        nueva_foto = Imagenes(hotel = nombre_hotel, url = elemento)
        #        nueva_foto.save()
        #else:
        #    aloj = Alojamiento.objects.get(id=int(identificador))
        #    aloj_nombre = aloj.nombre
            #print aloj_nombre
        #    if nombre == aloj_nombre:
        #        return (nombre, descripcion, web, telefono, direccion, cod_postal, categoria, subcategoria)


def ordenar_comentarios():
    aparcamientos = Aparcamiento.objects.all()
    dicc_aparcamiento_coment = {}
    for aparcamiento in aparcamientos:
        if aparcamiento.comentarios_set.count() != 0:
            dicc_aparcamiento_coment[aparcamiento.nombre] = aparcamiento.comentarios_set.count()
            # cuenta los comentarios que hay y los guardo en un diccionario
            # siendo el aparcamiento la clave y el valor el numero de comentarios
    if len(dicc_aparcamiento_coment) != 0:
        list_aparca_coment = dicc_hotel_coment.items() #lo tengo que pasar a lista para poder ordenarlo
        list_aparca_coment.sort(key=lambda x: x[1], reverse=True)

        if len(list_aparca_coment) >= 5:
            list_aparca_coment = list_aparca_coment[:10]
    else:
        list_aparca_coment = []

    return list_aparca_coment

def pag_principal(request):
    if request.method == "GET":
        #if Aparcamiento.objects.count() == 0:
        #    template = get_template('inicio.html')
        #    context = RequestContext(request)
        #    resp = template.render(context)
        #else:
            try:
                lista_usuarios = User.objects.all()
                lista_titulos = []
                for usu in lista_usuarios:
                    try:
                        cambio = Cambios.objects.get(usuario=usu.username)
                        if cambio.titulo != '':
                            titulo = cambio.titulo
                        else:
                            titulo = "Pagina de " + usu.username
                        lista_titulos.append((titulo, usu.username))
                    except:
                        titulo = "Pagina de " + usu.username
                        lista_titulos.append((titulo, usu.username))
            except:
                lista_usuarios = []
            lista_nombres_aparcamientos = ordenar_comentarios()
            if len(lista_nombres_aparcamientos) == 0:
                vacio = True
            else:
                vacio = False
            lista_aparcamientos = []
            for nombre in lista_nombres_aparcamientos:
                aparcamiento = Aparcamiento.objects.get(nombre = nombre[0])
                #try:
                #    fotos = Imagenes.objects.filter(hotel = hotel)
                #except ObjectDoesNotExist:
                #    fotos = []
                #if len(fotos) == 0:
                #    buena = ''
                #for foto in fotos:
                #    buena = foto.url
                lista_aparcamientos.append(aparcamiento)
                #lista_aparcamientos.append((aparcamiento, buena))
            template = get_template('pag_ppal.html')
            context = RequestContext(request, {'lista_aparcamientos': lista_aparcamientos, 'lista_titulos': lista_titulos, 'vacio': vacio})
            #context = RequestContext(request, {'lista_aparcamientos':  'lista_titulos'})
            resp = template.render(context)
            return HttpResponse(resp)

def pag_usuario(request, usuario):
    try:
        cambio = Cambio.objects.get(usuario=usuario)
        titulo = cambio.titulo
    except:
        titulo = ''
    aparc_usuario = Elegido.objects.filter(usuario = usuario)
    lista_aparcamientos = []
    for aparc in aparc_usuario:
        fecha = aloj.fecha
        aparcamiento = Aparcamiento.objects.get(nombre = aparc.aparcamiento.nombre)
        #try:
        #    fotos = Imagenes.objects.filter(hotel = hotel)
        #except ObjectDoesNotExist:
        #    fotos = []
        #if len(fotos) == 0:
        #    buena = ''
        #for foto in fotos:
        #    buena = foto.url
        #lista_aparcamientos.append((hotel, buena, fecha))
        lista_aparcamientos.append((aparcamiento))
    if len(lista_aparcamientos) == 0:
        vacio = True
    else:
        vacio = False

    template = get_template('pag_usuario.html')
    context = RequestContext(request, {'lista_aparcamientos': lista_aparcamientos, 'vacio': vacio, 'titulo': titulo, 'usuario':usuario})
    return HttpResponse(template.render(context))

@csrf_exempt
def pag_aparcamientos(request):
    if request.method == 'GET':
        aparcamientos = Aparcamiento.objects.all()

    elif request.method == 'POST':
        distrito = request.body.split('&')[7].split('=')[1]
        distrito = poner_espacios(categoria)[:-1]
        aparcamientos = Aparcamiento.objects.filter(distrito = distrito)


    lista_aparca=[]
    for aparc in aparcamientos:
        lista_aparca.append((aparc.nombre, aparc.id))

    template = get_template('pagina_aparcamientos.html')
    context = RequestContext(request, {'lista_aparcamientos': lista_aparcamientos})
    return HttpResponse(template.render(context))

def pag_aparcamiento(request, identificador):
    aparcamiento = Aparcamiento.objects.get(id = int(identificador))
    nombre = aparcamiento.nombre
    comentarios = Comentario.objects.filter(hotel = aparcamiento)
    if len(comentarios) != 0:
        Comentarios_vacio = False;
    else:
        Comentarios_vacio = True;
    try:
        coment_usu = Comentario.objects.get(aparcamiento = aparcamiento, usuario = request.user.username)
        NoComent = False
    except ObjectDoesNotExist:
        NoComent = True
    lista_comentarios=[]
    for coment in comentarios:
        lista_comentarios.append((coment.usuario, coment.texto, coment.fecha))

    visitas = contador_visitas(identificador)
    megustas = contador_megustas(identificador)
    template = get_template('pag_aparcamiento.html')
    context = RequestContext(request, {'aparcamiento': aparcamiento,'comentarios': lista_comentarios, 'NoComent': NoComent, 'Comentarios_vacio': Comentarios_vacio, 'visitas': visitas, 'megustas': megustas})
    return HttpResponse(template.render(context))

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

@csrf_exempt
def login(request):

    username = request.body.split('&')[1].split('=')[1]
    password = request.body.split('&')[2].split('=')[1]

    user = auth.authenticate(username=username, password=password)
    if user is not None:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect('/')
    else:
        template = get_template('error.html')
        return HttpResponse(template.render(Context({'texto': "Usuario no autenticado"})))

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



#def pag_xml(request, usuario):
#    aparcamientos_usuario = Elegido.objects.filter(usuario = usuario)
#    lista_todo = []
#    for aparca in aparcamientos_usuario:
#        lista_todo.append(aparca)
#    template = get_template('fichero_xml.xml')
#    context = RequestContext(request, {'lista_todo': lista_todo})
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
