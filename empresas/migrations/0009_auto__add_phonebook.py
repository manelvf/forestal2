# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PhoneBook'
        db.create_table('empresas_phonebook', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('empresas', ['PhoneBook'])


    def backwards(self, orm):
        
        # Deleting model 'PhoneBook'
        db.delete_table('empresas_phonebook')


    models = {
        'empresas.camion': {
            'Meta': {'object_name': 'Camion'},
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Empresa']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matricula': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'empresas.detallefactura': {
            'Meta': {'object_name': 'DetalleFactura'},
            'cantidad': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'concepto': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'factura': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Factura']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'servizo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Tala']", 'null': 'True', 'blank': 'True'}),
            'tipo_irpf': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tipo_irpf_set'", 'null': 'True', 'to': "orm['empresas.TipoIva']"}),
            'tipo_iva': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tipo_iva_set'", 'null': 'True', 'to': "orm['empresas.TipoIva']"}),
            'valor': ('django.db.models.fields.FloatField', [], {'blank': 'True'})
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
            'Meta': {'ordering': "['name']", 'object_name': 'Empresa'},
            'codigo_certificacion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'cp': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nif': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'obs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Provincia']"}),
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
        'empresas.phonebook': {
            'Meta': {'object_name': 'PhoneBook'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        'empresas.talonario': {
            'Meta': {'object_name': 'Talonario'},
            'PECL': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'destino': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Empresa']", 'null': 'True'}),
            'fin': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'recepcion': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
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
        'fincas.border': {
            'Meta': {'object_name': 'Border'},
            'borderFinca': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.BorderFinca']"}),
            'finca': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Finca']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.IntegerField', [], {})
        },
        'fincas.borderfinca': {
            'Meta': {'object_name': 'BorderFinca'},
            'agregado': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'concello': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Concello']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lugar': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['fincas.Lugar']", 'null': 'True', 'blank': 'True'}),
            'obs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parcela': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'poligon': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'ref_catastral': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'zona': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'fincas.concello': {
            'Meta': {'object_name': 'Concello'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Provincia']", 'null': 'True', 'blank': 'True'})
        },
        'fincas.condicioncorta': {
            'Meta': {'object_name': 'CondicionCorta'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'fincas.eventfinca': {
            'Meta': {'object_name': 'EventFinca'},
            'date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Empresa']", 'blank': 'True'}),
            'eventType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.EventFincaType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'obs': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'fincas.eventfincalog': {
            'Meta': {'object_name': 'EventFincaLog'},
            'eventfinca': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.EventFinca']"}),
            'finca': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Finca']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'fincas.eventfincatype': {
            'Meta': {'object_name': 'EventFincaType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'obs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        },
        'fincas.finca': {
            'Meta': {'unique_together': "(('concello', 'poligon', 'parcela', 'zona'),)", 'object_name': 'Finca'},
            'agregado': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'borders': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fincas.BorderFinca']", 'through': "orm['fincas.Border']", 'symmetrical': 'False'}),
            'calificacion_catastral': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'codigo_ref': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'concello': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Concello']"}),
            'cultivo_catastral': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'densidad': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'dono': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'finca_dono_set'", 'to': "orm['empresas.Empresa']"}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'finca_empresa_set'", 'to': "orm['empresas.Empresa']"}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fincas.EventFinca']", 'through': "orm['fincas.EventFincaLog']", 'symmetrical': 'False'}),
            'fecha_plantacion': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'ha_construidas': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ha_matorral': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ha_prado': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ha_total': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intensidad_catastral': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'lugar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Lugar']", 'null': 'True', 'blank': 'True'}),
            'modeloforestal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.ModeloForestal']"}),
            'monte': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Monte']", 'null': 'True', 'blank': 'True'}),
            'obs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'paraje_catastral': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'parcela': ('django.db.models.fields.IntegerField', [], {}),
            'pasado': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'poligon': ('django.db.models.fields.IntegerField', [], {}),
            'property_title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ref_catastral': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'relationships': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_to+'", 'symmetrical': 'False', 'through': "orm['fincas.Relationship']", 'to': "orm['fincas.Finca']"}),
            'superficie': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'unidade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Unidade']", 'null': 'True', 'blank': 'True'}),
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
        'fincas.monte': {
            'Meta': {'object_name': 'Monte'},
            'concello': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Concello']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lugar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Lugar']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parroquia': ('django.db.models.fields.related.ForeignKey', [], {'default': "''", 'to': "orm['fincas.Parroquia']", 'null': 'True', 'blank': 'True'})
        },
        'fincas.parroquia': {
            'Meta': {'object_name': 'Parroquia'},
            'concello': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Concello']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'fincas.provincia': {
            'Meta': {'object_name': 'Provincia'},
            'code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'fincas.relationship': {
            'Meta': {'object_name': 'Relationship'},
            'from_parcel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_parcel'", 'to': "orm['fincas.Finca']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.IntegerField', [], {}),
            'to_parcel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_parcel'", 'to': "orm['fincas.Finca']"})
        },
        'fincas.servizoforestaltipo': {
            'Meta': {'object_name': 'ServizoForestalTipo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fincas.tala': {
            'Meta': {'object_name': 'Tala'},
            'altura': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'codigoNORFOR': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'codigoPECL': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'comezo': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'condicions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['fincas.CondicionCorta']", 'null': 'True', 'blank': 'True'}),
            'dataPECL': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'dataPECLsaida': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'empresas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['empresas.Empresa']", 'null': 'True', 'blank': 'True'}),
            'entradaGrupo': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'final': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'finca': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Finca']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'm2_permiso': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'obs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'permiso': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.ServizoForestalTipo']"}),
            'tipocorta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.TipoCorta']", 'null': 'True', 'blank': 'True'}),
            'tm_permiso': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'viaxecamions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'viaxecamions'", 'to': "orm['fincas.ViaxeCamion']", 'db_table': "u'fincas_tala_viaxecamions'", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'})
        },
        'fincas.tipocorta': {
            'Meta': {'object_name': 'TipoCorta'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'fincas.unidade': {
            'Meta': {'object_name': 'Unidade'},
            'abrv': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'fincas.viaxecamion': {
            'Meta': {'object_name': 'ViaxeCamion'},
            'camion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Camion']", 'null': 'True', 'blank': 'True'}),
            'destino': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Empresa']", 'null': 'True', 'blank': 'True'}),
            'dia': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'estereo': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metrocubico': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'n_talonario': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'obs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'origen': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'origen'", 'to': "orm['fincas.Tala']", 'db_table': "u'fincas_tala_viaxecamions'", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'tm': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['empresas']
