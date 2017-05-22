#Lo adapto del barrapunto
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib2

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.incategoria = False
        self.insubcategoria = False
        self.inContent = True
        self.theContent = ""
        self.line = ""
        self.enlace = ""
        #self.lista_fotos = []
        self.aparcamiento= {}
        self.lista_aparcamientos = []

    def startElement (self, name, attrs):

        if name == 'service':
            if len(self.aparcamiento) != 0:
                self.lista_aparcamientos.append(self.aparcamiento)
                self.aparcamiento = {}
        elif name == 'item' and attrs.get('name') == 'Categoria':
            self.incategoria = True
        elif name == 'item' and attrs.get('name') == 'SubCategoria':
            self.insubcategoria = True


    def endElement (self, name):

        if name == 'multimedia':
            self.inmultimedia = False
            self.aparcamiento['url_fotos'] = self.lista_fotos # solo anado la lista al diccionario al final de todas las urls
            self.lista_fotos = []
        elif name == 'url':
            self.lista_fotos.append(self.theContent)
        elif self.incategoria:
            self.aparcamiento["Categoria"] = self.theContent
            self.theContent = ""
            self.incategoria = False
        elif self.insubcategoria:
            self.aparcamiento["SubCategoria"] = self.theContent
            self.theContent = ""
            self.insubcategoria = False
        else:
            if self.theContent != '':
                self.aparcamiento[name] = self.theContent
            self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


    def devuelve_lista (self):
        return self.lista_aparcamientos

# Load parser and driver
def parsear_fichero (fichero):
        #Load parser and driver
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    # Ready, set, go!
    archivo = urllib2.urlopen(fichero)
    theParser.parse(archivo)
    datos_aparcamientos = theHandler.devuelve_lista()
    return datos_aparcamientos
