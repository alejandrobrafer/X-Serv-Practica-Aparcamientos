"""PracticaFinal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from aparcamientos import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about$', views.about, name= "Pagina autoría práctica"),
    url(r'^$', views.pag_principal, name= "Pagina principal de la  practica"),
    url(r'cargar$', views.cargar_datos),
    url(r'cambiar_titulo', views.cambiar_titulo),
    url(r'.*/images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'templates/images/'}),
    url(r'.*/templates/styles\.css$', views.css),
    url(r'aparcamientos/templates/styles\.css$', views.css),
    url(r'templates/styles\.css', views.css),
    url(r'^login$', views.login),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^/aparcamientos$', views.pag_aparcamientos, name= "Pagina con todos los aparcamientos"),
    url(r'^/aparcamientos/(\d+)', views.pag_aparcamiento, name= "Pagina de un aparcamiento"),
    #url(r'^ppal_xml$', views.pag_xml),
    #url(r'^(.*)/xml$', views.pag_xml, name= "Canal XML"),
    url(r'^(.*)$', views.pag_usuario, name= "Pagina personal de un usuario"),
]
