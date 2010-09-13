from django.contrib import admin
from forestal2.ReadOnly import ReadOnlyAdminFields

from forestal2.fincas.models import Finca, Concello, Parroquia, Lugar, ModeloForestal, ServizoForestalTipo, Certificacion, ViaxeCamion, Especie, Tala

class FincaAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('concello', 'lugar', 'poligon', 'parcela')
    list_filter = ('concello', 'lugar', 'poligon', 'parcela')

class ConcelloAdmin(admin.ModelAdmin):
    pass

class TalaAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('finca', 'comezo', 'final', 'tipo')
    list_filter = ('comezo','final','permiso','tipo')
    date_hierarchy = 'comezo' 

admin.site.register(Finca, FincaAdmin)
admin.site.register(Concello)
admin.site.register(Parroquia)
admin.site.register(Lugar)
admin.site.register(ModeloForestal)
admin.site.register(ServizoForestalTipo)
admin.site.register(Certificacion)
admin.site.register(Especie)
admin.site.register(ViaxeCamion)
admin.site.register(Tala, TalaAdmin)

