import re

from django.core import serializers
from django.contrib import admin
from reversion.admin import VersionAdmin


from forestal2.ReadOnly import ReadOnlyAdminFields
from forestal2.fincas.models import Finca, Concello, Parroquia, Lugar, ModeloForestal, ServizoForestalTipo, Certificacion, ViaxeCamion, Especie, Tala, TalaForm, Unidade, Monte
from forestal2.memento.models import Memento

class FincaAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('concello', 'lugar', 'poligon', 'parcela','monte')
    list_filter = ('concello', 'lugar', 'poligon', 'parcela','monte')

class ConcelloAdmin(admin.ModelAdmin):
    pass

class TalaAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('finca', 'permiso', 'comezo', 'final', 'tipo','codigoPECL','get_viaxes')
    list_filter = ('permiso','comezo','final','tipo', 'dataPECL')
    date_hierarchy = 'comezo' 
    def get_form(self, request, obj=None, **kwargs):
        return TalaForm

class LugarAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name','parroquia','concello')
    list_filter = ('name','parroquia','concello')

class ViaxeCamionAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('dia','camion','tm','destino','get_concello','get_poligon','get_parcela','get_permission','get_monte')
    list_filter = ('dia','camion','tm','destino')


def save_model(self, request, obj, form, change):
    obj.save()

    m = re.match(r"[^(]*", self.model.__doc__)
    if m is not None:
        modelName = m.group()
    else:
        modelName = "Unable to retrieve"

    data = serializers.serialize("json", [obj, ])
    m = Memento(app="Fincas",model=modelName,data=data, user=request.user)
    m.save()
        
class UnidadeAdmin(admin.ModelAdmin):
    pass

UnidadeAdmin.save_model = save_model
FincaAdmin.save_model = save_model


admin.site.register(Finca, FincaAdmin)
admin.site.register(Concello)
admin.site.register(Parroquia)
admin.site.register(Lugar, LugarAdmin)
admin.site.register(ModeloForestal)
admin.site.register(ServizoForestalTipo)
admin.site.register(Certificacion)
admin.site.register(Especie)
admin.site.register(ViaxeCamion,ViaxeCamionAdmin)
admin.site.register(Tala, TalaAdmin)
admin.site.register(Unidade,UnidadeAdmin)
admin.site.register(Monte)

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
databrowse.site.register(Monte)
