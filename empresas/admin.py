from django.contrib import admin
from django.conf.urls import url, include

from empresas.models import TipoEmpresa, Empresa, Empleado, Camion, TipoOperacion, Factura, DetalleFactura, Recibo, DetalleRecibo, Provincia,TipoIva, Talonario, PhoneBook

class PhoneBookAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', )
    list_filter = ('number','name')

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


class TalonarioAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('recepcion', 'inicio', 'fin', 'PECL', 'destino')
    list_filter = ('recepcion', 'inicio', 'fin', 'PECL', 'destino')


admin.site.register(PhoneBook, PhoneBookAdmin)
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
admin.site.register(Talonario, TalonarioAdmin)


