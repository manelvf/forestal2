# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Unidade'
        """
        db.create_table('fincas_unidade', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('abrv', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('fincas', ['Unidade'])

        # Adding model 'Concello'
        db.create_table('fincas_concello', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('fincas', ['Concello'])

        # Adding model 'Parroquia'
        db.create_table('fincas_parroquia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('concello', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Concello'])),
        ))
        db.send_create_signal('fincas', ['Parroquia'])

        # Adding model 'Lugar'
        db.create_table('fincas_lugar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parroquia', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['fincas.Parroquia'], null=True, blank=True)),
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

        # Adding model 'Monte'
        db.create_table('fincas_monte', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parroquia', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['fincas.Parroquia'], null=True, blank=True)),
            ('concello', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Concello'])),
            ('lugar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Lugar'], blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('fincas', ['Monte'])

        # Adding model 'Finca'
        db.create_table('fincas_finca', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('concello', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Concello'])),
            ('lugar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Lugar'], null=True, blank=True)),
            ('poligon', self.gf('django.db.models.fields.IntegerField')()),
            ('parcela', self.gf('django.db.models.fields.IntegerField')()),
            ('agregado', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('zona', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('monte', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Monte'], null=True, blank=True)),
            ('superficie', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('codigo_ref', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('obs', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('modeloforestal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.ModeloForestal'])),
            ('fecha_plantacion', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('densidad', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('ha_matorral', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('ha_prado', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('ha_construidas', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('ha_total', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('dono', self.gf('django.db.models.fields.related.ForeignKey')(related_name='finca_dono_set', to=orm['empresas.Empresa'])),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(related_name='finca_empresa_set', to=orm['empresas.Empresa'])),
            ('unidade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Unidade'], null=True, blank=True)),
        ))
        db.send_create_signal('fincas', ['Finca'])

        # Adding model 'ServizoForestalTipo'
        db.create_table('fincas_servizoforestaltipo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('fincas', ['ServizoForestalTipo'])

        # Adding model 'Certificacion'
        db.create_table('fincas_certificacion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('finca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Finca'], null=True)),
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
            ('n_talonario', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('dia', self.gf('django.db.models.fields.DateField')()),
            ('camion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empresas.Camion'])),
            ('tm', self.gf('django.db.models.fields.FloatField')()),
            ('estereo', self.gf('django.db.models.fields.FloatField')()),
            ('metrocubico', self.gf('django.db.models.fields.FloatField')()),
            ('destino', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empresas.Empresa'])),
            ('obs', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('fincas', ['ViaxeCamion'])

        # Adding M2M table for field origen on 'ViaxeCamion'
        db.create_table(u'fincas_tala_viaxecamions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('viaxecamion', models.ForeignKey(orm['fincas.viaxecamion'], null=False)),
            ('tala', models.ForeignKey(orm['fincas.tala'], null=False))
        ))
        db.create_unique(u'fincas_tala_viaxecamions', ['viaxecamion_id', 'tala_id'])

        # Adding model 'Tala'
        db.create_table('fincas_tala', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comezo', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('final', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('permiso', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('codigoPECL', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('dataPECL', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('codigoNORFOR', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('tm_permiso', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('m2_permiso', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('finca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Finca'])),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.ServizoForestalTipo'])),
            ('obs', self.gf('django.db.models.fields.TextField')(blank=True)),
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
        db.create_table(u'fincas_tala_viaxecamions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tala', models.ForeignKey(orm['fincas.tala'], null=False)),
            ('viaxecamion', models.ForeignKey(orm['fincas.viaxecamion'], null=False))
        ))
        db.create_unique(u'fincas_tala_viaxecamions', ['tala_id', 'viaxecamion_id'])
        """


    def backwards(self, orm):
        
        # Deleting model 'Unidade'
        db.delete_table('fincas_unidade')

        # Deleting model 'Concello'
        db.delete_table('fincas_concello')

        # Deleting model 'Parroquia'
        db.delete_table('fincas_parroquia')

        # Deleting model 'Lugar'
        db.delete_table('fincas_lugar')

        # Deleting model 'ModeloForestal'
        db.delete_table('fincas_modeloforestal')

        # Deleting model 'Monte'
        db.delete_table('fincas_monte')

        # Deleting model 'Finca'
        db.delete_table('fincas_finca')

        # Deleting model 'ServizoForestalTipo'
        db.delete_table('fincas_servizoforestaltipo')

        # Deleting model 'Certificacion'
        db.delete_table('fincas_certificacion')

        # Deleting model 'Especie'
        db.delete_table('fincas_especie')

        # Deleting model 'ViaxeCamion'
        db.delete_table('fincas_viaxecamion')

        # Removing M2M table for field origen on 'ViaxeCamion'
        db.delete_table('fincas_tala_viaxecamions')

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
            'monte': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Monte']", 'null': 'True', 'blank': 'True'}),
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
        'fincas.servizoforestaltipo': {
            'Meta': {'object_name': 'ServizoForestalTipo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fincas.tala': {
            'Meta': {'object_name': 'Tala'},
            'codigoNORFOR': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'codigoPECL': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'comezo': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'dataPECL': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'empresas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['empresas.Empresa']", 'null': 'True', 'blank': 'True'}),
            'final': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'finca': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.Finca']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'm2_permiso': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'obs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'permiso': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.ServizoForestalTipo']"}),
            'tm_permiso': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'viaxecamions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'viaxecamions'", 'to': "orm['fincas.ViaxeCamion']", 'db_table': "u'fincas_tala_viaxecamions'", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'})
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
            'n_talonario': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'obs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'origen': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'origen'", 'to': "orm['fincas.Tala']", 'db_table': "u'fincas_tala_viaxecamions'", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'tm': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['fincas']
