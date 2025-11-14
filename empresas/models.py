from django.db import models
from django.conf import settings

class PhoneBook(models.Model):
    number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

# Create your models here.
class Provincia(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class TipoIva(models.Model):
    tipo = models.FloatField()
    def __str__(self):
        return str(self.tipo)

class TipoEmpresa(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    

class Empresa(models.Model):
    name = models.CharField(max_length=255)
    nif = models.CharField(max_length=25, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    cp = models.CharField(max_length=25, blank=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    telefonos = models.CharField(max_length=25, blank=True)
    obs = models.TextField(blank=True)
    tipoempresa = models.ForeignKey(TipoEmpresa, on_delete=models.CASCADE)
    codigo_certificacion = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Empleado(models.Model):
    name = models.CharField(max_length=25)
    apellido1 = models.CharField(max_length=25)
    apellido2 = models.CharField(max_length=25)
    nif = models.CharField(max_length=25)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Camion(models.Model):
    matricula = models.CharField(max_length=25)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    def __str__(self):
        return self.empresa.name + " " + str(self.matricula)

class TipoOperacion(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Factura(models.Model):
    empresa = models.ForeignKey(Empresa, related_name="factura_empresa_set", on_delete=models.CASCADE)
    cliente = models.ForeignKey(Empresa, related_name="factura_cliente_set", on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoOperacion, on_delete=models.CASCADE)
    numero = models.IntegerField()
    emision = models.DateField()
    
    def get_parcelas(self):
        from django.utils.html import format_html
        from django.utils.safestring import mark_safe
        from django.urls import reverse

        links = []
        b = self.detallefactura_set.all()

        for detail in b:
            if detail.servizo:
                try:
                    url = reverse('admin:fincas_tala_change', args=[detail.servizo.id])
                except:
                    url = f"/admin/fincas/tala/{detail.servizo.id}/change/"
                links.append(format_html('<a href="{}">{}</a>', url, str(detail)))

        return mark_safe('<br />'.join(links)) if links else ""

    get_parcelas.short_description = "Servizos"

    def __str__(self):
        return str(self.emision) + str(self.numero) + " - " + str(self.empresa) + " - " + str(self.cliente)  


class DetalleFactura(models.Model):
    #finca = models.ForeignKey("fincas.Finca", blank=True, null=True)
    servizo = models.ForeignKey("fincas.Tala", blank=True, null=True, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=255, blank=True)
    tipo_iva = models.ForeignKey("TipoIva",null=True, related_name="tipo_iva_set", blank=True, on_delete=models.CASCADE)
    tipo_irpf = models.ForeignKey("TipoIva", null=True, related_name="tipo_irpf_set", blank=True, on_delete=models.CASCADE)
    cantidad = models.FloatField(blank=True)
    valor = models.FloatField(blank=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.servizo) + " - " + str(self.concepto) + "  Fac: " + str(self.factura)

    
class Recibo(models.Model):
    numero = models.IntegerField()
    empresa = models.ForeignKey(Empresa, related_name="recibo_empresa_set", on_delete=models.CASCADE)
    cliente = models.ForeignKey(Empresa, related_name="recibo_cliente_set", on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoOperacion, on_delete=models.CASCADE)
    emision = models.DateField()
    def __str__(self):
        return str(self.numero)


class DetalleRecibo(models.Model):
    concepto = models.CharField(max_length=255)
    cantidad = models.FloatField()
    valor = models.FloatField()
    recibo = models.ForeignKey(Factura, on_delete=models.CASCADE)

class Talonario(models.Model):
		recepcion = models.DateField(auto_now = True)
		inicio = models.IntegerField(null=True)
		fin = models.IntegerField(null=True)
		PECL = models.BooleanField(default=True)
		destino = models.ForeignKey(Empresa, null=True, on_delete=models.CASCADE)

