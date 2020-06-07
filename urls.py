# test lines
# for git
import settings
from django.conf.urls import url, include
from django.urls import re_path, path
from django.views import static

from fincas.models import Finca, Concello, Parroquia, Lugar, ModeloForestal, ServizoForestalTipo, Certificacion, ViaxeCamion, Especie, Tala
from empresas.models import TipoEmpresa, Empresa, Empleado, Camion, TipoOperacion, Factura, DetalleFactura, Recibo, DetalleRecibo, Provincia,TipoIva

from fincas import views as fincasviews
from empresas import views as empresasviews
from memento import views as mementoviews



# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Example:
    # (r'^/', include('forestal2.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #(r'^homogeneidade/', 'forestal2.fincas.views.homogeneidade' ),
    re_path(r'^homogeneidade/(.*)/$', fincasviews.homogeneidade),

    url(r'^weightactions/$', fincasviews.weightActions),
    url(r'^weightactionsoutput/$', fincasviews.weightActionsOutput),

    url(r'^queryland$', fincasviews.queryland ),
    url(r'^queryland/(.*)/(.*)/(.*)/(.*)$', fincasviews.queryland ),
    url(r'^querycatastral/(.*)/(.*)/(.*)$', fincasviews.querycatastral ),
    url(r'listaviaxes/(?P<id>\d+)/$', fincasviews.listaviaxes, {}, 'listaviaxes-views'),
    url(r'assignfinca/(?P<id>\d+)/$', fincasviews.assignfinca),
    url(r'grid/(?P<id>\d+)/$', fincasviews.grid),
    url(r'grid/$', fincasviews.grid),
    url(r'grid$', fincasviews.grid),
    url(r'gridviaxe$', fincasviews.gridviaxe),
    url(r'gridviaxe/(?P<servizo>\d+)/$', fincasviews.gridviaxe),
    url(r'gridfinca$', fincasviews.gridfinca),
    url(r'joinviaxefinca$', fincasviews.joinviaxefinca),
    url(r'assocfincaservizo$', fincasviews.assocfincaservizo),
    url(r'assocservizocamion$', fincasviews.assocservizoviaxe),
    url(r'desassocviaxeservizo$', fincasviews.desassocviaxeservizo),

    url(r'^servizogridview$', fincasviews.servizogridview ),
    url(r'gridservizo$', fincasviews.gridservizo),

    url(r'^facturagridview$', empresasviews.facturagridview),
    url(r'gridfactura$', empresasviews.gridfactura),
    url(r'griddetallefactura$', empresasviews.griddetallefactura),
    url(r'griddetallefactura/(?P<id>\d+)/$', empresasviews.griddetallefactura),
    url(r'adddetallefactura/(?P<id>\d+)/$', empresasviews.adddetallefactura),
    url(r'adddetallefactura$', empresasviews.adddetallefactura),
    url(r'assocservizodetalle$', empresasviews.assocservizodetalle),

    #memento
    url(r'schred$', mementoviews.schred),

    # Deeds
    url(r'generateDeedCSV$', fincasviews.generateDeedCSV),

    url(r'exportGrid$', empresasviews.exportgrid),

    url(r'rewriteLandSize$', fincasviews.rewriteLandSize),

    url(r'^backup$', empresasviews.backup),

    # url(r'^admin_tools/', include('admin_tools.urls')),

    url(r'^site_media/(?P<path>.*)$', static.serve,
        {'document_root': settings.DOCUMENT_ROOT}),


    # Uncomment the next line to enable the admin:
    path('', admin.site.urls)

]

