# -*- coding: utf-8 -*-

from pprint import pprint
import datetime

from django.core import serializers
from django.utils.encoding import smart_unicode
from django.db import models
from django import forms

from forestal2.empresas.models import Empresa, Camion
from forestal2.settings import ENV_BASE_URL

class Unidade(models.Model):
    name = models.CharField(max_length=50)
    abrv = models.CharField(max_length=10)
    def __unicode__(self):
        return self.abrv or ""

class Provincia(models.Model):
		name = models.CharField(max_length=255, null=True, blank=True)
		code = models.CharField(max_length=5, null=True, blank=True, default="")
		def __unicode__(self):
				return (unicode(self.name) + u"-" + unicode(self.code)) or ""

class Concello(models.Model):
    name = models.CharField(max_length=255)
    provincia = models.ForeignKey(Provincia, null=True, blank=True)
    def __unicode__(self):
        return (unicode(self.name) + u"-" + unicode(self.provincia)) or ""

class Parroquia(models.Model):
    name = models.CharField(max_length=255)
    concello = models.ForeignKey(Concello)
    def __unicode__(self):
        return self.name + ", " + unicode(self.concello)

class Lugar(models.Model):
    name = models.CharField(max_length=255)
    parroquia = models.ForeignKey(Parroquia, blank=True, null=True, default="")
    concello = models.ForeignKey(Concello)
    def __unicode__(self):
        return self.name + u", " + unicode(self.parroquia) 
    
class ModeloForestal(models.Model):
    name = models.CharField(max_length=100)
    obs = models.TextField()
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = "Modelo Forestal"


class Monte(models.Model):
    parroquia = models.ForeignKey(Parroquia, blank=True, null=True, default="")
    concello = models.ForeignKey(Concello)
    lugar = models.ForeignKey(Lugar,blank=True)
    name = models.CharField(max_length=100, blank=True, default="")
    number = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.number) + u':' + unicode(self.name)


class BorderFinca(models.Model):
    concello = models.ForeignKey(Concello,blank=True)
    lugar = models.ForeignKey(Lugar,blank=True,null=True)
    poligon = models.IntegerField()
    parcela = models.IntegerField()
    agregado = models.IntegerField(blank=True)
    zona = models.IntegerField(blank=True)
    ref_catastral = models.CharField(max_length=255, default="", blank=True)
    obs = models.TextField(blank=True)


class Deed(models.Model):
    date = models.DateField(blank=True)
    number = models.IntegerField()
    buyer =  models.ForeignKey(Empresa)
    fincas = models.ManyToManyField('Finca', through='DeedFinca', null=True)
    price = models.FloatField(blank=True, null=True)
    obs = models.TextField(blank=True)

class EventFincaType(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")
    order = models.IntegerField()
    obs = models.TextField(blank=True)

class EventFinca(models.Model):
    date = models.DateField(blank=True)
    empresa = models.ForeignKey(Empresa, blank=True)
    obs = models.TextField(blank=True)
    eventType = models.ForeignKey(EventFincaType)


class EventFincaLog(models.Model):
    eventfinca = models.ForeignKey(EventFinca)
    finca = models.ForeignKey('Finca')


class Finca(models.Model):
    concello = models.ForeignKey(Concello)
    lugar = models.ForeignKey(Lugar,blank=True,null=True)
    poligon = models.IntegerField()
    parcela = models.IntegerField()
    agregado = models.IntegerField(blank=True)
    zona = models.IntegerField(blank=True)
    monte = models.ForeignKey(Monte,blank=True,null=True)
    superficie = models.FloatField(blank=True)
    codigo_ref = models.CharField(max_length=255, default="", blank=True)
    ref_catastral = models.CharField(max_length=255, default="", blank=True)
    pasado = models.NullBooleanField()
    obs = models.TextField(blank=True)
    modeloforestal = models.ForeignKey(ModeloForestal, verbose_name = "Modelo Forestal")
    fecha_plantacion = models.DateField(blank=True)
    densidad = models.FloatField(blank=True)
    ha_matorral = models.FloatField(blank=True)
    ha_prado = models.FloatField(blank=True)
    ha_construidas = models.FloatField(blank=True)
    ha_total = models.FloatField(blank=True)
    dono = models.ForeignKey(Empresa, related_name="finca_dono_set")
    empresa = models.ForeignKey(Empresa, related_name="finca_empresa_set")
    unidade = models.ForeignKey(Unidade,blank=True,null=True)
    paraje_catastral = models.CharField(max_length=255, default="", blank=True)
    cultivo_catastral = models.CharField(max_length=255, default="", blank=True)
    intensidad_catastral = models.CharField(max_length=255, default="", blank=True)
    calificacion_catastral= models.CharField(max_length=255, default="", blank=True)

    borders = models.ManyToManyField(BorderFinca, through='Border')

    events = models.ManyToManyField(EventFinca, through='EventFincaLog')

    relationships = models.ManyToManyField('self', through='Relationship', 
                                           symmetrical=False, 
                                           related_name='related_to+')


    class Meta:
        verbose_name = "Parcela"
        unique_together = ("concello", "poligon", "parcela", "zona")

    def __unicode__(self):
        s = ""
        """
        if self.concello is not None:
            s += self.concello.name + " - "

        if self.lugar:
            s += " Parroquia: " + unicode(self.lugar.parroquia) + " Lugar: " + unicode(self.lugar.name) + " . "
        """

        return str(self.pk) + " Pol: " + str(self.poligon) + ", Par:" +str(self.parcela)


    def add_relationship(self, parcel, owner):
        relationship, created = Relationship.objects.get_or_create(
            from_parcel=self,
            to_parcel=parcel,
            owner=owner)
        relationship, created = Relationship.objects.get_or_create(
            from_parcel=person,
            to_parcel=self,
            owner=owner)
        return relationship

    def remove_relationship(self, parcel, owner):
        Relationship.objects.filter(
            from_parcel=self, 
            to_parcel=parcel,
            owner=owner).delete()
        Relationship.objects.filter(
            to_parcel=self, 
            from_parcel=parcel,
            status=status).delete()
        return

    def get_relationships(self):
        return self.relationships.filter(
            to_parcel__from_parcel=self)
    


OWNER_SAME = 1
OWNER_DIFFERENT = 2
RELATIONSHIP_STATUSES = (
    (OWNER_SAME, 'Same Owner'),
    (OWNER_DIFFERENT, 'Different Owner'),
)


class Border(models.Model):
    borderFinca = models.ForeignKey(BorderFinca)
    finca = models.ForeignKey(Finca)
    owner = models.IntegerField(choices=RELATIONSHIP_STATUSES)


class DeedFinca(models.Model):
    deed = models.ForeignKey(Deed)
    finca = models.ForeignKey(Finca)


class Relationship(models.Model):
    # Relations between parcels
    from_parcel = models.ForeignKey(Finca, related_name='from_parcel')
    to_parcel = models.ForeignKey(Finca, related_name='to_parcel')

    owner = models.IntegerField(choices=RELATIONSHIP_STATUSES)


class ServizoForestalTipo(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name



class Certificacion(models.Model):
    finca = models.ForeignKey(Finca, null=True)
    envio_documentacion = models.DateField()
    aprobacion = models.DateField();
    def __unicode__(self):
        return unicode(self.finca) + " // Envio: " + unicode(self.envio_documentacion) + " // Aprobacion: " + unicode(self.aprobacion)


class Especie(models.Model):
    name = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name


class ViaxeCamion(models.Model):
    n_talonario = models.PositiveIntegerField(null=True, blank=True, verbose_name=u"Nº talonario")
    dia = models.DateField(null=True, blank=True)
    camion = models.ForeignKey(Camion,null=True, blank=True)
    tm = models.FloatField(null=True, blank=True)
    estereo = models.FloatField(null=True, blank=True)
    metrocubico = models.FloatField(null=True, blank=True)
    destino = models.ForeignKey(Empresa, null=True, blank=True)
    origen = models.ManyToManyField('Tala', related_name="origen", db_table=u'fincas_tala_viaxecamions', blank=True, null=True)
    obs = models.TextField(blank=True)

    def get_permission(self):
        s = ""

        k = self.origen.all()
        if len(k) > 0:
            s = unicode(k[0].permiso)

        return s

    get_permission.short_description = u"Data Permiso"

    def get_concello(self):
        s = ""

        k = self.origen.all()
        if len(k) > 0:
            s = unicode(k[0].finca.concello)

        return s

    get_concello.short_description = u"Concello"

    def get_poligon(self):
        s = ""

        k = self.origen.all()
        if len(k) > 0:
            s = unicode(k[0].finca.poligon)

        return s

    get_poligon.short_description = u"Poligono"

    def get_parcela(self):
        s = ""

        k = self.origen.all()
        if len(k) > 0:
            s = unicode(k[0].finca.parcela)

        return s

    get_parcela.short_description = u"Parcela"

    def get_monte(self):
        s = ""

        k = self.origen.all()
        if len(k) > 0:
            s = unicode(k[0].finca.monte)
            if s == "None":
                s = ""

        return s

    get_monte.short_description = u"Monte"


    def __unicode__(self):
        #return unicode(self.dia) + " " + unicode(self.camion) + " - Tm: " + unicode(self.tm)
        return unicode(self.pk) + u" - " + unicode(self.dia) + " " + " - Tm: " + unicode(self.tm)


class TipoCorta(models.Model):
		name = models.CharField(max_length=100, blank=True, verbose_name = u"Tipo de corta")

class CondicionCorta(models.Model):
		name = models.CharField(max_length=100, blank=True, verbose_name = u"Condicion")
    
# Formerly Permiso Forestal
class Tala(models.Model):
    comezo = models.DateField(blank=True)
    final = models.DateField(blank=True)
    permiso = models.DateField(blank=True)
    entradaGrupo = models.DateField(blank=True)
    codigoPECL = models.CharField(max_length=100, blank=True)
    dataPECL = models.DateField(blank=True)
    codigoNORFOR = models.CharField(max_length=100, blank=True, verbose_name=u"NORFOR")
    dataPECLsaida = models.DateField(blank=True, null=True, verbose_name=u"Alb. Saida PECL")

    tm_permiso = models.FloatField(verbose_name=u"Pes permiso", blank=True, default=0)
    m2_permiso = models.FloatField(verbose_name=u"m3 permiso", default=0)
    altura = models.IntegerField(default=0, null=True,blank=True)

    tipocorta = models.ForeignKey(TipoCorta, null=True, blank=True)
    condicions = models.ManyToManyField(CondicionCorta, blank=True, null=True)

    empresas = models.ManyToManyField(Empresa, blank=True, null=True)
    viaxecamions = models.ManyToManyField(ViaxeCamion, related_name="viaxecamions", db_table=u'fincas_tala_viaxecamions', blank=True, null=True)
    finca = models.ForeignKey(Finca)
    tipo = models.ForeignKey(ServizoForestalTipo)
    obs = models.TextField(blank=True)
    
    def get_viaxes(self):
        n = self.viaxecamions.exclude(camion__exact=None)
        v = self.viaxecamions.all()

        return unicode(u'<a href="' + ENV_BASE_URL + '/listaviaxes/' + unicode(self.id) + '" >' +
               unicode(len(n)) + u'</a>' +
							 u'/' +
               u'<a href="' + ENV_BASE_URL + '/listaviaxes/' + unicode(self.id) + '" >' +
               unicode(len(v)) + u'</a>')

    get_viaxes.short_description = u'N Viaxes'
    get_viaxes.allow_tags = True


    class Meta:
        verbose_name = "Servizo Forestal"
    def __unicode__(self):
        if len(self.codigoPECL) > 0:
            pecl = u'S'
        else:
            pecl = u'N'

        #return unicode(self.tipo) + u" - " + unicode(self.finca) + u" / desde " + unicode(self.comezo) + " ata " + unicode (self.final) + ". Permiso: " + unicode(self.permiso) + u'. PECL: ' + pecl + u'. NORFOR: ' + unicode(self.codigoNORFOR)
        return unicode(self.pk) + u" - " + u" / desde " + unicode(self.comezo) + " ata " + unicode (self.final) + ". Permiso: " + unicode(self.permiso) + u'. PECL: ' + pecl + u'. NORFOR: ' + unicode(self.codigoNORFOR)


class TalaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TalaForm, self).__init__(*args, **kwargs)
        
        if self.initial.has_key('comezo'):
            self.fields['viaxecamions'].queryset =  ViaxeCamion.objects.filter(dia__gte = self.initial['comezo'])

    class Meta:
        model = Tala


