# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CondicionCorta'
        db.create_table('fincas_condicioncorta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('fincas', ['CondicionCorta'])

        # Adding M2M table for field condicions on 'Tala'
        db.create_table('fincas_tala_condicions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tala', models.ForeignKey(orm['fincas.tala'], null=False)),
            ('condicioncorta', models.ForeignKey(orm['fincas.condicioncorta'], null=False))
        ))
        db.create_unique('fincas_tala_condicions', ['tala_id', 'condicioncorta_id'])


    def backwards(self, orm):
        
        # Deleting model 'CondicionCorta'
        db.delete_table('fincas_condicioncorta')

        # Removing M2M table for field condicions on 'Tala'
        db.delete_table('fincas_tala_condicions')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Provincia']", 'null': 'True', 'blank': 'True'})
        },
        'fincas.condicioncorta': {
            'Meta': {'object_name': 'CondicionCorta'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'fincas.especie': {
            'Meta': {'object_name': 'Especie'},
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fincas.finca': {
            'Meta': {'unique_together': "(('concello', 'poligon', 'parcela', 'zona'),)", 'object_name': 'Finca'},
            'agregado': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'calificacion_catastral': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'codigo_ref': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'concello': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Concello']"}),
            'cultivo_catastral': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'densidad': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'dono': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'finca_dono_set'", 'to': "orm['empresas.Empresa']"}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'finca_empresa_set'", 'to': "orm['empresas.Empresa']"}),
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
            'ref_catastral': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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
        'fincas.servizoforestaltipo': {
            'Meta': {'object_name': 'ServizoForestalTipo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fincas.tala': {
            'Meta': {'object_name': 'Tala'},
            'altura': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'codigoNORFOR': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'codigoPECL': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'comezo': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'condicions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['fincas.CondicionCorta']", 'null': 'True', 'blank': 'True'}),
            'dataPECL': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'dataPECLsaida': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'empresas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['empresas.Empresa']", 'null': 'True', 'blank': 'True'}),
            'final': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'finca': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Finca']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'm2_permiso': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'obs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'permiso': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.ServizoForestalTipo']"}),
            'tipocorta': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.TipoCorta']", 'null': 'True'}),
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

    complete_apps = ['fincas']
