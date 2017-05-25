#Lo adapto del barrapunto
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
from xml.sax.saxutils import escape, unescape
import urllib.request

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.dataType = 'contenido'

        self.inContent = True
        self.theContent = ""

        self.dataSection = ['NOMBRE', 'DESCRIPCION', 'ACCESIBILIDAD', 'CONTENT-URL','BARRIO', 'DISTRITO',
        'LATITUD', 'LONGITUD', 'TELEFONO', 'EMAIL']
        self.inSection = False
        self.atrSection = ''

        self.lista_aparcamientos = {}
        self.aparcamiento = []

    def startElement (self, name, attrs):

        if name == 'atributo' and attrs['nombre'] in self.dataSection:
            self.atrSection = attrs['nombre']
            self.inSection = True
        elif name == 'atributo' and (attrs['nombre'] == 'LOCALIZACION' or attrs['nombre'] == 'DATOSCONTACTOS') and attrs['nombre'] in self.dataSection:
            self.atrSection = attrs['nombre']
            self.inSection = True



    def endElement (self, name):

        if name == 'atributo' and self.atrSection in self.dataSection:
            self.lista_aparcamientos[self.atrSection] = self.theContent
            self.atrSection = ""
        if name == 'atributo'and (self.atrSection == 'LOCALIZACION' or self.atrSection == 'DATOSCONTACTOS') and self.atrSection in self.dataSection:
            self.lista_aparcamientos[self.atrSection] = self.theContent
            self.atrSection = ""

        if name == self.dataType:
            self.aparcamiento.append(self.lista_aparcamientos)
            self.lista_aparcamientos = {}
        if self.inSection:
            self.inSection = False
            self.atrSection = ""
            self.theContent = ""

    def characters (self, chars):
        html_escape_table = {
            "&quot;" : '"',
            "&apos;" : "'",
            "&iexcl" : u'¡',
            "&iquest" : u'¿',
            "&aacute;" : u'á',
            "&iacute;" : u'í',
            "&oacute;" : u'ó',
            "&uacute;" : u'ú',
            "&eacute;" : u'é',
            "&ntilde;" : u'ñ',
            "&Ntilde;" : u'Ñ',
            "&Aacute;" : u'Á',
            "&Iacute;" : u'Í',
            "&Oacute;" : u'Ó',
            "&Uacute;" : u'Ú',
            "&Eacute;" : u'É',
            "&Ocirc;" : u'Ô',
            "&ocirc;" : u"ô",
            "&uuml;" : u'ü',
            "&Uuml;" : u'Ü',
            "&nbsp;" : '\n',
            "&rdquo;" : '"',
            "&ldquo;" : '"',
            "&lsquo;" : "'",
            "&rsquo;" : "'",
        }
        if self.inSection:
         text = self.theContent + chars
         self.theContent = unescape(text, html_escape_table)




# Load parser and driver
def parsear_fichero (fichero):
        #Load parser and driver
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    # Ready, set, go!
    archivo = urllib.request.urlopen(fichero)
    theParser.parse(archivo)
    datos_aparcamientos = theHandler.aparcamiento
    return datos_aparcamientos
