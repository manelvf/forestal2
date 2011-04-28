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
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^databrowse/(.*)', databrowse.site.root),
    #(r'^homogeneidade/', 'forestal2.fincas.views.homogeneidade' ),
    (r'^homogeneidade/(.*)/$', 'forestal2.fincas.views.homogeneidade' ),
    (r'^queryland$', 'forestal2.fincas.views.queryland' ),
    (r'^queryland/(.*)/(.*)/(.*)/(.*)$', 'forestal2.fincas.views.queryland' ),
    (r'^querycatastral/(.*)/(.*)/(.*)$', 'forestal2.fincas.views.querycatastral' ),
    (r'listaviaxes/(?P<id>\d+)/$', 'forestal2.fincas.views.listaviaxes', {}, 'listaviaxes-views'),
    (r'assignfinca/(?P<id>\d+)/$', 'forestal2.fincas.views.assignfinca'),
    (r'grid/(?P<id>\d+)/$', 'forestal2.fincas.views.grid'),
    (r'grid$', 'forestal2.fincas.views.grid'),
    (r'gridviaxe$', 'forestal2.fincas.views.gridviaxe'),
    (r'joinviaxefinca$', 'forestal2.fincas.views.joinviaxefinca'),

    (r'^admin_tools/', include('admin_tools.urls')),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': '/Users/manel/Sites/virtualenvs/oficina/forestal2/media'}),


    # Uncomment the next line to enable the admin:
    (r'^', include(admin.site.urls))

)

"""
DEPRECATED
urlpatterns += patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'index.html'})
)
"""
