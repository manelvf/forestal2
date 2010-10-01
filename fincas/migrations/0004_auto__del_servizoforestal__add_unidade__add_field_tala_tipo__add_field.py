# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'ServizoForestal'
        db.delete_table('fincas_servizoforestal')

        # Adding model 'Unidade'
        db.create_table('fincas_unidade', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('abrv', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('fincas', ['Unidade'])

        # Adding field 'Tala.tipo'
        db.add_column('fincas_tala', 'tipo', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['fincas.ServizoForestalTipo']), keep_default=False)

        # Adding field 'Tala.obs'
        db.add_column('fincas_tala', 'obs', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Changing field 'Tala.final'
        db.alter_column('fincas_tala', 'final', self.gf('django.db.models.fields.DateField')(blank=True))

        # Adding field 'ViaxeCamion.destino'
        db.add_column('fincas_viaxecamion', 'destino', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['empresas.Empresa']), keep_default=False)

        # Adding field 'Finca.dono'
        db.add_column('fincas_finca', 'dono', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='finca_dono_set', to=orm['empresas.Empresa']), keep_default=False)

        # Adding field 'Finca.empresa'
        db.add_column('fincas_finca', 'empresa', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='finca_empresa_set', to=orm['empresas.Empresa']), keep_default=False)

        # Changing field 'Finca.superficie'
        db.alter_column('fincas_finca', 'superficie', self.gf('django.db.models.fields.FloatField')(blank=True))


    def backwards(self, orm):
        
        # Adding model 'ServizoForestal'
        db.create_table('fincas_servizoforestal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('final', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.ServizoForestalTipo'])),
            ('comezo', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('fincas', ['ServizoForestal'])

        # Deleting model 'Unidade'
        db.delete_table('fincas_unidade')

        # Deleting field 'Tala.tipo'
        db.delete_column('fincas_tala', 'tipo_id')

        # Deleting field 'Tala.obs'
        db.delete_column('fincas_tala', 'obs')

        # Changing field 'Tala.final'
        db.alter_column('fincas_tala', 'final', self.gf('django.db.models.fields.DateField')())

        # Deleting field 'ViaxeCamion.destino'
        db.delete_column('fincas_viaxecamion', 'destino_id')

        # Deleting field 'Finca.dono'
        db.delete_column('fincas_finca', 'dono_id')

        # Deleting field 'Finca.empresa'
        db.delete_column('fincas_finca', 'empresa_id')

        # Changing field 'Finca.superficie'
        db.alter_column('fincas_finca', 'superficie', self.gf('django.db.models.fields.IntegerField')(blank=True))


    models = {
        'empresas.camion': {
            'Meta': {'object_name': 'Camion'},
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Empresa']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matricula': ('django.db.models.fields.CharField', [], {'max_length': '25'})
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
        'empresas.provincia': {
            'Meta': {'object_name': 'Provincia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'finca': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Finca']", 'null': 'True'}),
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
        },
        'fincas.servizoforestaltipo': {
            'Meta': {'object_name': 'ServizoForestalTipo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fincas.tala': {
            'Meta': {'object_name': 'Tala'},
            'comezo': ('django.db.models.fields.DateField', [], {}),
            'empresas': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['empresas.Empresa']"}),
            'final': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'finca': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Finca']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'obs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'permiso': ('django.db.models.fields.DateField', [], {}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.ServizoForestalTipo']"}),
            'tm_permiso': ('django.db.models.fields.FloatField', [], {}),
            'viaxecamions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['fincas.ViaxeCamion']", 'blank': 'True'})
        },
        'fincas.unidade': {
            'Meta': {'object_name': 'Unidade'},
            'abrv': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'fincas.viaxecamion': {
            'Meta': {'object_name': 'ViaxeCamion'},
            'camion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Camion']"}),
            'destino': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['empresas.Empresa']"}),
            'dia': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tm': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['fincas']
