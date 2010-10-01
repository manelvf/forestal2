# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'DetalleFactura.finca'
        db.add_column('empresas_detallefactura', 'finca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Finca'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'DetalleFactura.finca'
        db.delete_column('empresas_detallefactura', 'finca_id')


    models = {
        'empresas.camion': {
            'Meta': {'object_name': 'Camion'},
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Empresa']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matricula': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'empresas.detallefactura': {
            'Meta': {'object_name': 'DetalleFactura'},
            'cantidad': ('django.db.models.fields.FloatField', [], {}),
            'concepto': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'factura': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Factura']"}),
            'finca': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Finca']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'valor': ('django.db.models.fields.FloatField', [], {})
        },
        'empresas.detallerecibo': {
            'Meta': {'object_name': 'DetalleRecibo'},
            'cantidad': ('django.db.models.fields.FloatField', [], {}),
            'concepto': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recibo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Factura']"}),
            'valor': ('django.db.models.fields.FloatField', [], {})
        },
        'empresas.empleado': {
            'Meta': {'object_name': 'Empleado'},
            'apellido1': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'apellido2': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Empresa']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'nif': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'empresas.empresa': {
            'Meta': {'object_name': 'Empresa'},
            'codigo_certificacion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'cp': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nif': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'obs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Provincia']", 'blank': 'True'}),
            'telefonos': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'tipoempresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.TipoEmpresa']"})
        },
        'empresas.factura': {
            'Meta': {'object_name': 'Factura'},
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'factura_cliente_set'", 'to': "orm['empresas.Empresa']"}),
            'emision': ('django.db.models.fields.DateField', [], {}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'factura_empresa_set'", 'to': "orm['empresas.Empresa']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero': ('django.db.models.fields.IntegerField', [], {}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.TipoOperacion']"})
        },
        'empresas.provincia': {
            'Meta': {'object_name': 'Provincia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'empresas.recibo': {
            'Meta': {'object_name': 'Recibo'},
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recibo_cliente_set'", 'to': "orm['empresas.Empresa']"}),
            'emision': ('django.db.models.fields.DateField', [], {}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recibo_empresa_set'", 'to': "orm['empresas.Empresa']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero': ('django.db.models.fields.IntegerField', [], {}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.TipoOperacion']"})
        },
        'empresas.tipoempresa': {
            'Meta': {'object_name': 'TipoEmpresa'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'empresas.tipoiva': {
            'Meta': {'object_name': 'TipoIva'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.FloatField', [], {})
        },
        'empresas.tipooperacion': {
            'Meta': {'object_name': 'TipoOperacion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'fincas.concello': {
            'Meta': {'object_name': 'Concello'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'fincas.finca': {
            'Meta': {'object_name': 'Finca'},
            'agregado': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'codigo_ref': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'concello': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Concello']"}),
            'densidad': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'dono': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'finca_dono_set'", 'to': "orm['empresas.Empresa']"}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'finca_empresa_set'", 'to': "orm['empresas.Empresa']"}),
            'fecha_plantacion': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'ha_construidas': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ha_matorral': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ha_prado': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ha_total': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lugar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Lugar']", 'null': 'True', 'blank': 'True'}),
            'modeloforestal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.ModeloForestal']"}),
            'obs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parcela': ('django.db.models.fields.IntegerField', [], {}),
            'poligon': ('django.db.models.fields.IntegerField', [], {}),
            'superficie': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'zona': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'fincas.lugar': {
            'Meta': {'object_name': 'Lugar'},
            'concello': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Concello']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parroquia': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': "orm['fincas.Parroquia']", 'null': 'True', 'blank': 'True'})
        },
        'fincas.modeloforestal': {
            'Meta': {'object_name': 'ModeloForestal'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'obs': ('django.db.models.fields.TextField', [], {})
        },
        'fincas.parroquia': {
            'Meta': {'object_name': 'Parroquia'},
            'concello': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Concello']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['empresas']
