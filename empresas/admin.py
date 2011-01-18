from django.contrib import admin
from forestal2.empresas.models import TipoEmpresa, Empresa, Empleado, Camion, TipoOperacion, Factura, DetalleFactura, Recibo, DetalleRecibo, Provincia,TipoIva 


class EmpresaAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name', 'direccion', 'tipoempresa')
    list_filter = ('name', 'direccion', 'tipoempresa')

class DetalleFacturaAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('servizo', 'concepto', 'factura')
    list_filter = ('servizo', 'concepto', 'factura')

class DetalleTabularAdmin(admin.TabularInline):
    model = DetalleFactura
    #fk_name = "finca"


class FacturaAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('empresa', 'cliente', 'tipo', 'numero', 'emision','get_parcelas')
    list_filter = ('empresa', 'cliente', 'tipo', 'numero', 'emision')
    inlines = [
        DetalleTabularAdmin,
    ]
    

admin.site.register(TipoEmpresa)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Empleado)
admin.site.register(Camion)
admin.site.register(TipoOperacion)
admin.site.register(Factura, FacturaAdmin)
admin.site.register(DetalleFactura, DetalleFacturaAdmin)
admin.site.register(Recibo)
admin.site.register(DetalleRecibo)
admin.site.register(Provincia)
admin.site.register(TipoIva)


from django.contrib import databrowse

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

