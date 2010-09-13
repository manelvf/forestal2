from django.db import models
from forestal2.empresas.models import Empresa, Camion
from django.utils.encoding import smart_unicode


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
        return self.name
    
class ModeloForestal(models.Model):
    name = models.CharField(max_length=100)
    obs = models.TextField()
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = "Modelo Forestal"


# Create your models here.
class Finca(models.Model):
    concello = models.ForeignKey(Concello)
    lugar = models.ForeignKey(Lugar,blank=True,null=True)
    poligon = models.IntegerField()
    parcela = models.IntegerField()
    agregado = models.IntegerField(blank=True)
    zona = models.IntegerField(blank=True)
    superficie = models.IntegerField(blank=True)
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
    destino = models.ForeignKey(Empresa)
    def __unicode__(self):
        return unicode(self.dia) + " " + unicode(self.camion) + " - Tm: " + unicode(self.tm)
    
# Formerly Permiso Forestal
class Tala(models.Model):
    comezo = models.DateField()
    final = models.DateField(blank=True)
    permiso = models.DateField()
    tm_permiso = models.FloatField(verbose_name=u"Tm/pes permiso")
    empresas = models.ManyToManyField(Empresa)
    viaxecamions = models.ManyToManyField(ViaxeCamion, blank=True)
    finca = models.ForeignKey(Finca)
    tipo = models.ForeignKey(ServizoForestalTipo)
    obs = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Servizo Forestal"
    def __unicode__(self):
        return str(self.tipo) + " // " + unicode(self.comezo) + " // " + unicode (self.final)

