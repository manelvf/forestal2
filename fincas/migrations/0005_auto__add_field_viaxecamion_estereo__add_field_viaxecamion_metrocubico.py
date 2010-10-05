# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'ViaxeCamion.estereo'
        db.add_column('fincas_viaxecamion', 'estereo', self.gf('django.db.models.fields.FloatField')(default=0), keep_default=False)

        # Adding field 'ViaxeCamion.metrocubico'
        db.add_column('fincas_viaxecamion', 'metrocubico', self.gf('django.db.models.fields.FloatField')(default=0), keep_default=False)

        # Adding field 'ViaxeCamion.obs'
        db.add_column('fincas_viaxecamion', 'obs', self.gf('django.db.models.fields.TextField')(default=0, blank=True), keep_default=False)

        # Adding M2M table for field origen on 'ViaxeCamion'
        db.create_table(u'fincas_tala_viaxecamions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('viaxecamion', models.ForeignKey(orm['fincas.viaxecamion'], null=False)),
            ('tala', models.ForeignKey(orm['fincas.tala'], null=False))
        ))
        db.create_unique(u'fincas_tala_viaxecamions', ['viaxecamion_id', 'tala_id'])

        # Adding field 'Finca.unidade'
        db.add_column('fincas_finca', 'unidade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Unidade'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'ViaxeCamion.estereo'
        db.delete_column('fincas_viaxecamion', 'estereo')

        # Deleting field 'ViaxeCamion.metrocubico'
        db.delete_column('fincas_viaxecamion', 'metrocubico')

        # Deleting field 'ViaxeCamion.obs'
        db.delete_column('fincas_viaxecamion', 'obs')

        # Removing M2M table for field origen on 'ViaxeCamion'
        db.delete_table('fincas_tala_viaxecamions')

        # Deleting field 'Finca.unidade'
        db.delete_column('fincas_finca', 'unidade_id')


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
            'viaxecamions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'viaxecamions'", 'null': 'True', 'db_table': "u'fincas_tala_viaxecamions'", 'to': "orm['fincas.ViaxeCamion']"})
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
            'estereo': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metrocubico': ('django.db.models.fields.FloatField', [], {}),
            'obs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'origen': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'origen'", 'null': 'True', 'db_table': "u'fincas_tala_viaxecamions'", 'to': "orm['fincas.Tala']"}),
            'tm': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['fincas']
