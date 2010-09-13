# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Concello'
        db.create_table('fincas_concello', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('fincas', ['Concello'])

        # Adding model 'Lugar'
        db.create_table('fincas_lugar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parroquia', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('concello', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Concello'])),
        ))
        db.send_create_signal('fincas', ['Lugar'])

        # Adding model 'ModeloForestal'
        db.create_table('fincas_modeloforestal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('obs', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('fincas', ['ModeloForestal'])

        # Adding model 'ServizoForestal'
        db.create_table('fincas_servizoforestal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comezo', self.gf('django.db.models.fields.DateField')()),
            ('final', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('fincas', ['ServizoForestal'])

        # Adding model 'Finca'
        db.create_table('fincas_finca', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lugar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Lugar'])),
            ('poligon', self.gf('django.db.models.fields.IntegerField')()),
            ('parcela', self.gf('django.db.models.fields.IntegerField')()),
            ('agregado', self.gf('django.db.models.fields.IntegerField')()),
            ('zona', self.gf('django.db.models.fields.IntegerField')()),
            ('superficie', self.gf('django.db.models.fields.IntegerField')()),
            ('codigo_ref', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('obs', self.gf('django.db.models.fields.TextField')()),
            ('modeloforestal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.ModeloForestal'])),
            ('fecha_plantacion', self.gf('django.db.models.fields.DateField')()),
            ('densidad', self.gf('django.db.models.fields.FloatField')()),
            ('ha_matorral', self.gf('django.db.models.fields.FloatField')()),
            ('ha_prado', self.gf('django.db.models.fields.FloatField')()),
            ('ha_construidas', self.gf('django.db.models.fields.FloatField')()),
            ('ha_total', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('fincas', ['Finca'])

        # Adding model 'Certificacion'
        db.create_table('fincas_certificacion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('finca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Finca'])),
            ('envio_documentacion', self.gf('django.db.models.fields.DateField')()),
            ('aprobacion', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('fincas', ['Certificacion'])

        # Adding model 'Especie'
        db.create_table('fincas_especie', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('codigo', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('fincas', ['Especie'])

        # Adding model 'ViaxeCamion'
        db.create_table('fincas_viaxecamion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dia', self.gf('django.db.models.fields.DateField')()),
            ('camion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empresas.Camion'])),
            ('tm', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('fincas', ['ViaxeCamion'])

        # Adding model 'Tala'
        db.create_table('fincas_tala', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comezo', self.gf('django.db.models.fields.DateField')()),
            ('final', self.gf('django.db.models.fields.DateField')()),
            ('permiso', self.gf('django.db.models.fields.DateField')()),
            ('tm_permiso', self.gf('django.db.models.fields.FloatField')()),
            ('finca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Finca'])),
        ))
        db.send_create_signal('fincas', ['Tala'])

        # Adding M2M table for field empresas on 'Tala'
        db.create_table('fincas_tala_empresas', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tala', models.ForeignKey(orm['fincas.tala'], null=False)),
            ('empresa', models.ForeignKey(orm['empresas.empresa'], null=False))
        ))
        db.create_unique('fincas_tala_empresas', ['tala_id', 'empresa_id'])

        # Adding M2M table for field viaxecamions on 'Tala'
        db.create_table('fincas_tala_viaxecamions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tala', models.ForeignKey(orm['fincas.tala'], null=False)),
            ('viaxecamion', models.ForeignKey(orm['fincas.viaxecamion'], null=False))
        ))
        db.create_unique('fincas_tala_viaxecamions', ['tala_id', 'viaxecamion_id'])


    def backwards(self, orm):
        
        # Deleting model 'Concello'
        db.delete_table('fincas_concello')

        # Deleting model 'Lugar'
        db.delete_table('fincas_lugar')

        # Deleting model 'ModeloForestal'
        db.delete_table('fincas_modeloforestal')

        # Deleting model 'ServizoForestal'
        db.delete_table('fincas_servizoforestal')

        # Deleting model 'Finca'
        db.delete_table('fincas_finca')

        # Deleting model 'Certificacion'
        db.delete_table('fincas_certificacion')

        # Deleting model 'Especie'
        db.delete_table('fincas_especie')

        # Deleting model 'ViaxeCamion'
        db.delete_table('fincas_viaxecamion')

        # Deleting model 'Tala'
        db.delete_table('fincas_tala')

        # Removing M2M table for field empresas on 'Tala'
        db.delete_table('fincas_tala_empresas')

        # Removing M2M table for field viaxecamions on 'Tala'
        db.delete_table('fincas_tala_viaxecamions')


    models = {
        'empresas.camion': {
            'Meta': {'object_name': 'Camion'},
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Empresa']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matricula': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'empresas.empresa': {
            'Meta': {'object_name': 'Empresa'},
            'codigo_certificacion': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cp': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nif': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'obs': ('django.db.models.fields.TextField', [], {}),
            'provincia': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'telefonos': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'tipoempresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.TipoEmpresa']"})
        },
        'empresas.tipoempresa': {
            'Meta': {'object_name': 'TipoEmpresa'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'fincas.certificacion': {
            'Meta': {'object_name': 'Certificacion'},
            'aprobacion': ('django.db.models.fields.DateField', [], {}),
            'envio_documentacion': ('django.db.models.fields.DateField', [], {}),
            'finca': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Finca']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'fincas.concello': {
            'Meta': {'object_name': 'Concello'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'fincas.especie': {
            'Meta': {'object_name': 'Especie'},
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fincas.finca': {
            'Meta': {'object_name': 'Finca'},
            'agregado': ('django.db.models.fields.IntegerField', [], {}),
            'codigo_ref': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'densidad': ('django.db.models.fields.FloatField', [], {}),
            'fecha_plantacion': ('django.db.models.fields.DateField', [], {}),
            'ha_construidas': ('django.db.models.fields.FloatField', [], {}),
            'ha_matorral': ('django.db.models.fields.FloatField', [], {}),
            'ha_prado': ('django.db.models.fields.FloatField', [], {}),
            'ha_total': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lugar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Lugar']"}),
            'modeloforestal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.ModeloForestal']"}),
            'obs': ('django.db.models.fields.TextField', [], {}),
            'parcela': ('django.db.models.fields.IntegerField', [], {}),
            'poligon': ('django.db.models.fields.IntegerField', [], {}),
            'superficie': ('django.db.models.fields.IntegerField', [], {}),
            'zona': ('django.db.models.fields.IntegerField', [], {})
        },
        'fincas.lugar': {
            'Meta': {'object_name': 'Lugar'},
            'concello': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Concello']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parroquia': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'fincas.modeloforestal': {
            'Meta': {'object_name': 'ModeloForestal'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'obs': ('django.db.models.fields.TextField', [], {})
        },
        'fincas.servizoforestal': {
            'Meta': {'object_name': 'ServizoForestal'},
            'comezo': ('django.db.models.fields.DateField', [], {}),
            'final': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'fincas.tala': {
            'Meta': {'object_name': 'Tala'},
            'comezo': ('django.db.models.fields.DateField', [], {}),
            'empresas': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['empresas.Empresa']"}),
            'final': ('django.db.models.fields.DateField', [], {}),
            'finca': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Finca']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permiso': ('django.db.models.fields.DateField', [], {}),
            'tm_permiso': ('django.db.models.fields.FloatField', [], {}),
            'viaxecamions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fincas.ViaxeCamion']"})
        },
        'fincas.viaxecamion': {
            'Meta': {'object_name': 'ViaxeCamion'},
            'camion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Camion']"}),
            'dia': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tm': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['fincas']
