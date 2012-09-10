from django.db import models
from forestal2.settings import ENV_BASE_URL


# Create your models here.
class Provincia(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class TipoIva(models.Model):
    tipo = models.FloatField()
    def __unicode__(self):
        return unicode(self.tipo)

class TipoEmpresa(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name
    

class Empresa(models.Model):
    name = models.CharField(max_length=255)
    nif = models.CharField(max_length=25, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    cp = models.CharField(max_length=25, blank=True)
    provincia = models.ForeignKey(Provincia, blank=True)
    telefonos = models.CharField(max_length=25, blank=True)
    obs = models.TextField(blank=True)
    tipoempresa = models.ForeignKey(TipoEmpresa)
    codigo_certificacion = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name


class Empleado(models.Model):
    name = models.CharField(max_length=25)
    apellido1 = models.CharField(max_length=25)
    apellido2 = models.CharField(max_length=25)
    nif = models.CharField(max_length=25)
    empresa = models.ForeignKey(Empresa)
    def __unicode__(self):
        return self.name

class Camion(models.Model):
    matricula = models.CharField(max_length=25)
    empresa = models.ForeignKey(Empresa)
    def __unicode__(self):
        return self.empresa.name + " " + unicode(self.matricula)

class TipoOperacion(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class Factura(models.Model):
    empresa = models.ForeignKey(Empresa, related_name="factura_empresa_set")
    cliente = models.ForeignKey(Empresa, related_name="factura_cliente_set")
    tipo = models.ForeignKey(TipoOperacion)
    numero = models.IntegerField()
    emision = models.DateField()
    
    def get_parcelas(self):
        s = ""

        b = self.detallefactura_set.all()
        if len(b) > 0:
            for k in b:
                s += u'<a href="'+ ENV_BASE_URL +'/fincas/tala/'+unicode(k.servizo.id)+'" >' + unicode(k) + u'</a> <br />'

        return s

    get_parcelas.short_description = u"Servizos"
    get_parcelas.allow_tags=True

    def __unicode__(self):
        return unicode(self.emision) + unicode(self.numero) + u" - " + unicode(self.empresa) + u" - " + unicode(self.cliente)  


class DetalleFactura(models.Model):
    #finca = models.ForeignKey("fincas.Finca", blank=True, null=True)
    servizo = models.ForeignKey("fincas.Tala", blank=True, null=True)
    concepto = models.CharField(max_length=255, blank=True)
    tipo_iva = models.ForeignKey("TipoIva",null=True, related_name="tipo_iva_set", blank=True)
    tipo_irpf = models.ForeignKey("TipoIva", null=True, related_name="tipo_irpf_set", blank=True)
    cantidad = models.FloatField(blank=True)
    valor = models.FloatField(blank=True)
    factura = models.ForeignKey(Factura)
    def __unicode__(self):
        return unicode(self.servizo) + u" - " + unicode(self.concepto) + u"  Fac: " + unicode(self.factura)

    
class Recibo(models.Model):
    numero = models.IntegerField()
    empresa = models.ForeignKey(Empresa, related_name="recibo_empresa_set")
    cliente = models.ForeignKey(Empresa, related_name="recibo_cliente_set")
    tipo = models.ForeignKey(TipoOperacion)
    emision = models.DateField()
    def __unicode__(self):
        return unicode(self.numero)


class DetalleRecibo(models.Model):
    concepto = models.CharField(max_length=255)
    cantidad = models.FloatField()
    valor = models.FloatField()
    recibo = models.ForeignKey(Factura)

class Talonario(models.Model):
		recepcion = models.DateField(auto_now = True)
		inicio = models.IntegerField(null=True)
		fin = models.IntegerField(null=True)
		PECL = models.BooleanField(default=True)
		destino = models.ForeignKey(Empresa, null=True)

