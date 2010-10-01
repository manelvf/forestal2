# test lines
# for git
from django.conf.urls.defaults import *

from forestal2.fincas.models import Finca, Concello, Parroquia, Lugar, ModeloForestal, ServizoForestalTipo, Certificacion, ViaxeCamion, Especie, Tala
from forestal2.empresas.models import TipoEmpresa, Empresa, Empleado, Camion, TipoOperacion, Factura, DetalleFactura, Recibo, DetalleRecibo, Provincia,TipoIva 

from django.contrib import databrowse
databrowse.site.register(Finca)
databrowse.site.register(Concello)
databrowse.site.register(Parroquia)
databrowse.site.register(Lugar)
databrowse.site.register(ModeloForestal)
databrowse.site.register(ServizoForestalTipo)
databrowse.site.register(Certificacion)
databrowse.site.register(Especie)
databrowse.site.register(ViaxeCamion)
databrowse.site.register(Tala)

databrowse.site.register(TipoEmpresa)
databrowse.site.register(Empresa)
databrowse.site.register(Empleado)
databrowse.site.register(Camion)
databrowse.site.register(TipoOperacion)
databrowse.site.register(Factura)
databrowse.site.register(DetalleFactura)
databrowse.site.register(Recibo)
databrowse.site.register(DetalleRecibo)
databrowse.site.register(Provincia)
databrowse.site.register(TipoIva)


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^forestal2/', include('forestal2.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^', include(admin.site.urls)),
    (r'^databrowse/(.*)', databrowse.site.root),

)

"""
DEPRECATED
urlpatterns += patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'index.html'})
)
"""
