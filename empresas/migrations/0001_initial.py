# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Provincia'
        db.create_table('empresas_provincia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('empresas', ['Provincia'])

        # Adding model 'TipoEmpresa'
        db.create_table('empresas_tipoempresa', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('empresas', ['TipoEmpresa'])

        # Adding model 'Empresa'
        db.create_table('empresas_empresa', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('nif', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('cp', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('provincia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empresas.Provincia'], blank=True)),
            ('telefonos', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('obs', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tipoempresa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empresas.TipoEmpresa'])),
            ('codigo_certificacion', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('empresas', ['Empresa'])

        # Adding model 'Empleado'
        db.create_table('empresas_empleado', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('apellido1', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('apellido2', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('nif', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empresas.Empresa'])),
        ))
        db.send_create_signal('empresas', ['Empleado'])

        # Adding model 'Camion'
        db.create_table('empresas_camion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('matricula', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empresas.Empresa'])),
        ))
        db.send_create_signal('empresas', ['Camion'])

        # Adding model 'TipoOperacion'
        db.create_table('empresas_tipooperacion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('empresas', ['TipoOperacion'])

        # Adding model 'Factura'
        db.create_table('empresas_factura', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(related_name='factura_empresa_set', to=orm['empresas.Empresa'])),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='factura_cliente_set', to=orm['empresas.Empresa'])),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empresas.TipoOperacion'])),
            ('numero', self.gf('django.db.models.fields.IntegerField')()),
            ('emision', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('empresas', ['Factura'])

        # Adding model 'DetalleFactura'
        db.create_table('empresas_detallefactura', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('concepto', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cantidad', self.gf('django.db.models.fields.FloatField')()),
            ('valor', self.gf('django.db.models.fields.FloatField')()),
            ('factura', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empresas.Factura'])),
        ))
        db.send_create_signal('empresas', ['DetalleFactura'])

        # Adding model 'Recibo'
        db.create_table('empresas_recibo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('numero', self.gf('django.db.models.fields.IntegerField')()),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recibo_empresa_set', to=orm['empresas.Empresa'])),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recibo_cliente_set', to=orm['empresas.Empresa'])),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empresas.TipoOperacion'])),
            ('emision', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('empresas', ['Recibo'])

        # Adding model 'DetalleRecibo'
        db.create_table('empresas_detallerecibo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('concepto', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cantidad', self.gf('django.db.models.fields.FloatField')()),
            ('valor', self.gf('django.db.models.fields.FloatField')()),
            ('recibo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empresas.Factura'])),
        ))
        db.send_create_signal('empresas', ['DetalleRecibo'])


    def backwards(self, orm):
        
        # Deleting model 'Provincia'
        db.delete_table('empresas_provincia')

        # Deleting model 'TipoEmpresa'
        db.delete_table('empresas_tipoempresa')

        # Deleting model 'Empresa'
        db.delete_table('empresas_empresa')

        # Deleting model 'Empleado'
        db.delete_table('empresas_empleado')

        # Deleting model 'Camion'
        db.delete_table('empresas_camion')

        # Deleting model 'TipoOperacion'
        db.delete_table('empresas_tipooperacion')

        # Deleting model 'Factura'
        db.delete_table('empresas_factura')

        # Deleting model 'DetalleFactura'
        db.delete_table('empresas_detallefactura')

        # Deleting model 'Recibo'
        db.delete_table('empresas_recibo')

        # Deleting model 'DetalleRecibo'
        db.delete_table('empresas_detallerecibo')


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
        'empresas.tipooperacion': {
            'Meta': {'object_name': 'TipoOperacion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['empresas']
