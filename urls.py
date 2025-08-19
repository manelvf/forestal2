# test lines
# for git
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog
from django.views.static import serve
from django.views.generic import TemplateView

# Import view functions
from fincas import views as fincas_views
from empresas import views as empresas_views

from fincas.models import Finca, Concello, Parroquia, Lugar, ModeloForestal, ServizoForestalTipo, Certificacion, ViaxeCamion, Especie, Tala
from empresas.models import TipoEmpresa, Empresa, Empleado, Camion, TipoOperacion, Factura, DetalleFactura, Recibo, DetalleRecibo, Provincia,TipoIva 



# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Vue.js SPA - serve the main app for all non-API routes
    path('', TemplateView.as_view(template_name='vue_app.html'), name='vue_app'),
    
    # API endpoints (keep existing functionality)
    re_path(r'^api/homogeneidade/(.*)/$', fincas_views.homogeneidade),
    re_path(r'^api/weightactions/$', fincas_views.weightActions),
    re_path(r'^api/weightactionsoutput/$', fincas_views.weightActionsOutput),
    re_path(r'^api/queryland$', fincas_views.queryland),
    re_path(r'^api/queryland/(.*)/(.*)/(.*)/(.*)$', fincas_views.queryland),
    re_path(r'^api/querycatastral/(.*)/(.*)/(.*)$', fincas_views.querycatastral),
    re_path(r'^api/listaviaxes/(?P<id>\d+)/$', fincas_views.listaviaxes, name='listaviaxes-views'),
    re_path(r'^api/assignfinca/(?P<id>\d+)/$', fincas_views.assignfinca),
    re_path(r'^api/grid/(?P<id>\d+)/$', fincas_views.grid),
    re_path(r'^api/grid/$', fincas_views.grid),
    re_path(r'^api/grid$', fincas_views.grid),
    re_path(r'^api/gridviaxe$', fincas_views.gridviaxe),
    re_path(r'^api/gridviaxe/(?P<servizo>\d+)/$', fincas_views.gridviaxe),
    re_path(r'^api/gridfinca$', fincas_views.gridfinca),
    re_path(r'^api/joinviaxefinca$', fincas_views.joinviaxefinca),
    re_path(r'^api/assocfincaservizo$', fincas_views.assocfincaservizo),
    re_path(r'^api/assocservizocamion$', fincas_views.assocservizoviaxe),
    re_path(r'^api/desassocviaxeservizo$', fincas_views.desassocviaxeservizo),
    re_path(r'^api/servizogridview$', fincas_views.servizogridview),
    re_path(r'^api/gridservizo$', fincas_views.gridservizo),
    re_path(r'^api/facturagridview$', empresas_views.facturagridview),
    re_path(r'^api/gridfactura$', empresas_views.gridfactura),
    re_path(r'^api/griddetallefactura$', empresas_views.griddetallefactura),
    re_path(r'^api/griddetallefactura/(?P<id>\d+)/$', empresas_views.griddetallefactura),
    re_path(r'^api/adddetallefactura/(?P<id>\d+)/$', empresas_views.adddetallefactura),
    re_path(r'^api/adddetallefactura$', empresas_views.adddetallefactura),
    re_path(r'^api/assocservizodetalle$', empresas_views.assocservizodetalle),
    re_path(r'^api/generateDeedCSV$', fincas_views.generateDeedCSV),
    re_path(r'^api/exportGrid$', empresas_views.exportgrid),
    re_path(r'^api/rewriteLandSize$', fincas_views.rewriteLandSize),
    re_path(r'^api/backup$', empresas_views.backup),

    # Legacy routes for direct access (keep for backward compatibility)
    re_path(r'^legacy/homogeneidade/(.*)/$', fincas_views.homogeneidade),
    re_path(r'^legacy/weightactions/$', fincas_views.weightActions),
    re_path(r'^legacy/servizogridview$', fincas_views.servizogridview),
    re_path(r'^legacy/facturagridview$', empresas_views.facturagridview),

    # Admin URLs
    path('admin/', admin.site.urls),
    re_path(r'^admin/jsi18n/$', JavaScriptCatalog.as_view()),

    # Static files
    re_path(r'^site_media/(?P<path>.*)$', serve,
        {'document_root': settings.DOCUMENT_ROOT}),

]

# Static files (CSS, JavaScript, Images)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
