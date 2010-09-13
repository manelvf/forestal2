from django.contrib import admin
from forestal2.empresas.models import TipoEmpresa, Empresa, Empleado, Camion, TipoOperacion, Factura, DetalleFactura, Recibo, DetalleRecibo, Provincia,TipoIva 


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('name', 'tipoempresa')
    list_filter = ('name', 'tipoempresa')


admin.site.register(TipoEmpresa)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Empleado)
admin.site.register(Camion)
admin.site.register(TipoOperacion)
admin.site.register(Factura)
admin.site.register(DetalleFactura)
admin.site.register(Recibo)
admin.site.register(DetalleRecibo)
admin.site.register(Provincia)
admin.site.register(TipoIva)


