import re

from django.core import serializers
from django.contrib import admin
from django.contrib import databrowse
from reversion.admin import VersionAdmin


from forestal2.ReadOnly import ReadOnlyAdminFields
from forestal2.fincas.models import Finca, Provincia, Concello, Parroquia, Lugar, ModeloForestal, ServizoForestalTipo, Certificacion, ViaxeCamion, Especie, Tala, TalaForm, Unidade, Monte, TipoCorta, Relationship, BorderFinca, Border, Deed, EventFinca, EventFincaType, DeedFinca, EventFincaTimeline
from forestal2.empresas.models import Empresa, TipoEmpresa
from forestal2.memento.models import Memento


class RelationshipInline(admin.StackedInline):
    model = Relationship
    #fk_name = 'from_parcel'

class BorderInline(admin.TabularInline):
    model = Border 
    fk_name = 'finca'


class DeedFincaInline(admin.StackedInline):
    model = DeedFinca
    fk_name = 'deed'
    #fields = ('finca', 'deed',)

class DeedFinca2Inline(admin.StackedInline):
    model = DeedFinca
    fk_name = 'finca'


class EventFincaTimelineInline(admin.StackedInline):
    model = EventFincaTimeline
    #fk_name = 'eventfinca'


class FincaAdmin(VersionAdmin):
    save_as = True
    list_display = ('concello', 'lugar', 'poligon', 'parcela','monte','pasado')
    list_filter = ('concello', 'lugar', 'poligon', 'parcela','monte','pasado')
    inlines = [BorderInline, DeedFinca2Inline, EventFincaTimelineInline]


#class DeedFincaAdmin(VersionAdmin):
#    inlines = [DeedFincaInline]

class DeedAdmin(VersionAdmin):
    inlines = [DeedFincaInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print db_field.name
        if db_field.name == "buyer":
            kwargs["queryset"] = Empresa.objects.filter(tipoempresa__name="Particular")
        return super(DeedAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class BorderFincaAdmin(VersionAdmin):
    pass


class ProvinciaAdmin(admin.ModelAdmin):
    pass


class ConcelloAdmin(admin.ModelAdmin):
    pass


class TalaAdmin(VersionAdmin):
    save_as = True
    list_display = ('finca', 'entradaGrupo', 'permiso', 'comezo', 'final', 'tipo','codigoPECL','codigoNORFOR','get_viaxes','tm_permiso','m2_permiso')
    list_filter = ('permiso','entradaGrupo','comezo','final','tipo', 'dataPECL')
    #date_hierarchy = 'comezo' 
    list_per_page = 25
    def get_form(self, request, obj=None, **kwargs):
        return TalaForm

class LugarAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name','parroquia','concello')
    list_filter = ('name','parroquia','concello')

class ViaxeCamionAdmin(VersionAdmin):
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
admin.site.register(BorderFinca, BorderFincaAdmin)
admin.site.register(Deed, DeedAdmin)
admin.site.register(DeedFinca)
admin.site.register(EventFinca)
admin.site.register(EventFincaType)
admin.site.register(Concello)
admin.site.register(Provincia)
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
admin.site.register(TipoCorta)


"""
DataBrowse
"""
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
