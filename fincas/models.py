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


class Concello(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name or ""

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
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)


# Create your models here.
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

    class Meta:
        verbose_name = "Parcela"
    def __unicode__(self):
        s = ""
        if self.concello is not None:
            s += self.concello.name + " - "
        if self.lugar:
            s +=  " Parroquia: " + unicode(self.lugar.parroquia) + " Lugar: " + unicode(self.lugar.name) + " . "

        return s + " Pol: " + str(self.poligon) + ", Parcela:" +str(self.parcela)


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
    dia = models.DateField()
    camion = models.ForeignKey(Camion)
    tm = models.FloatField()
    estereo = models.FloatField()
    metrocubico = models.FloatField()
    destino = models.ForeignKey(Empresa)
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
        return unicode(self.dia) + " " + unicode(self.camion) + " - Tm: " + unicode(self.tm)


    
# Formerly Permiso Forestal
class Tala(models.Model):
    comezo = models.DateField()
    final = models.DateField(blank=True)
    permiso = models.DateField()
    tm_permiso = models.FloatField(verbose_name=u"Pes permiso")
    m2_permiso = models.FloatField(verbose_name=u"m3 permiso", default=0)
    empresas = models.ManyToManyField(Empresa)
    viaxecamions = models.ManyToManyField(ViaxeCamion, related_name="viaxecamions", db_table=u'fincas_tala_viaxecamions', blank=True, null=True)
    finca = models.ForeignKey(Finca)
    tipo = models.ForeignKey(ServizoForestalTipo)
    obs = models.TextField(blank=True)
    
    def get_viaxes(self):
        v = self.viaxecamions.all()

        return u'<a href="' + ENV_BASE_URL + '/listaviaxes/' + unicode(self.id) + '" >' + unicode(len(v)) + u'</a>'

    get_viaxes.short_description = u'N Viaxes'
    get_viaxes.allow_tags = True


    class Meta:
        verbose_name = "Servizo Forestal"
    def __unicode__(self):
        return unicode(self.tipo) + u" - " + unicode(self.finca) + u" / desde " + unicode(self.comezo) + " ata " + unicode (self.final)


class TalaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TalaForm, self).__init__(*args, **kwargs)
        
        if self.initial.has_key('comezo'):
            self.fields['viaxecamions'].queryset =  ViaxeCamion.objects.filter(dia__gte = self.initial['comezo'])

    class Meta:
        model = Tala


