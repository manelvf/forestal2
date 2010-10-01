from django.contrib import admin
from forestal2.empresas.models import TipoEmpresa, Empresa, Empleado, Camion, TipoOperacion, Factura, DetalleFactura, Recibo, DetalleRecibo, Provincia,TipoIva 


class EmpresaAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name', 'direccion', 'tipoempresa')
    list_filter = ('name', 'direccion', 'tipoempresa')

class DetalleFacturaAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('finca', 'concepto', 'factura')
    list_filter = ('finca', 'concepto', 'factura')

class FacturaAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('empresa', 'cliente', 'tipo', 'numero', 'emision')
    list_filter = ('empresa', 'cliente', 'tipo', 'numero', 'emision')
    

admin.site.register(TipoEmpresa)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Empleado)
admin.site.register(Camion)
admin.site.register(TipoOperacion)
admin.site.register(Factura)
admin.site.register(DetalleFactura, DetalleFacturaAdmin)
admin.site.register(Recibo)
admin.site.register(DetalleRecibo)
admin.site.register(Provincia)
admin.site.register(TipoIva)


