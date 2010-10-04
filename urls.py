# test lines
# for git
from django.conf.urls.defaults import *
from django.contrib import databrowse

from forestal2.fincas.models import Finca, Concello, Parroquia, Lugar, ModeloForestal, ServizoForestalTipo, Certificacion, ViaxeCamion, Especie, Tala
from forestal2.empresas.models import TipoEmpresa, Empresa, Empleado, Camion, TipoOperacion, Factura, DetalleFactura, Recibo, DetalleRecibo, Provincia,TipoIva 



# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^forestal2/', include('forestal2.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^forestal/admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^forestal/databrowse/(.*)', databrowse.site.root),
    (r'^forestal/homogeneidade/', 'forestal2.fincas.views.homogeneidade' ),

    # Uncomment the next line to enable the admin:
    (r'^forestal/', include(admin.site.urls)),

)

"""
DEPRECATED
urlpatterns += patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'index.html'})
)
"""
