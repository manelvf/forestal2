# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ServizoForestalTipo'
        db.create_table('fincas_servizoforestaltipo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('fincas', ['ServizoForestalTipo'])

        # Adding model 'Parroquia'
        db.create_table('fincas_parroquia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('concello', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Concello'])),
        ))
        db.send_create_signal('fincas', ['Parroquia'])

        # Renaming column for 'Lugar.parroquia' to match new field type.
        db.rename_column('fincas_lugar', 'parroquia', 'parroquia_id')
        # Changing field 'Lugar.parroquia'
        db.alter_column('fincas_lugar', 'parroquia_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Parroquia'], null=True, blank=True))

        # Adding index on 'Lugar', fields ['parroquia']
        db.create_index('fincas_lugar', ['parroquia_id'])

        # Changing field 'Certificacion.finca'
        db.alter_column('fincas_certificacion', 'finca_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Finca'], null=True))

        # Adding field 'ServizoForestal.tipo'
        db.add_column('fincas_servizoforestal', 'tipo', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['fincas.ServizoForestalTipo']), keep_default=False)

        # Changing field 'ServizoForestal.final'
        db.alter_column('fincas_servizoforestal', 'final', self.gf('django.db.models.fields.DateField')(blank=True))

        # Adding field 'Finca.concello'
        db.add_column('fincas_finca', 'concello', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['fincas.Concello']), keep_default=False)

        # Changing field 'Finca.ha_prado'
        db.alter_column('fincas_finca', 'ha_prado', self.gf('django.db.models.fields.FloatField')(blank=True))

        # Changing field 'Finca.lugar'
        db.alter_column('fincas_finca', 'lugar_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Lugar'], null=True, blank=True))

        # Changing field 'Finca.zona'
        db.alter_column('fincas_finca', 'zona', self.gf('django.db.models.fields.IntegerField')(blank=True))

        # Changing field 'Finca.obs'
        db.alter_column('fincas_finca', 'obs', self.gf('django.db.models.fields.TextField')(blank=True))

        # Changing field 'Finca.ha_matorral'
        db.alter_column('fincas_finca', 'ha_matorral', self.gf('django.db.models.fields.FloatField')(blank=True))

        # Changing field 'Finca.codigo_ref'
        db.alter_column('fincas_finca', 'codigo_ref', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True))

        # Changing field 'Finca.fecha_plantacion'
        db.alter_column('fincas_finca', 'fecha_plantacion', self.gf('django.db.models.fields.DateField')(blank=True))

        # Changing field 'Finca.ha_total'
        db.alter_column('fincas_finca', 'ha_total', self.gf('django.db.models.fields.FloatField')(blank=True))

        # Changing field 'Finca.ha_construidas'
        db.alter_column('fincas_finca', 'ha_construidas', self.gf('django.db.models.fields.FloatField')(blank=True))

        # Changing field 'Finca.densidad'
        db.alter_column('fincas_finca', 'densidad', self.gf('django.db.models.fields.FloatField')(blank=True))

        # Changing field 'Finca.superficie'
        db.alter_column('fincas_finca', 'superficie', self.gf('django.db.models.fields.IntegerField')(blank=True))

        # Changing field 'Finca.agregado'
        db.alter_column('fincas_finca', 'agregado', self.gf('django.db.models.fields.IntegerField')(blank=True))


    def backwards(self, orm):
        
        # Deleting model 'ServizoForestalTipo'
        db.delete_table('fincas_servizoforestaltipo')

        # Deleting model 'Parroquia'
        db.delete_table('fincas_parroquia')

        # Renaming column for 'Lugar.parroquia' to match new field type.
        db.rename_column('fincas_lugar', 'parroquia_id', 'parroquia')
        # Changing field 'Lugar.parroquia'
        db.alter_column('fincas_lugar', 'parroquia', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Removing index on 'Lugar', fields ['parroquia']
        db.delete_index('fincas_lugar', ['parroquia_id'])

        # Changing field 'Certificacion.finca'
        db.alter_column('fincas_certificacion', 'finca_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Finca']))

        # Deleting field 'ServizoForestal.tipo'
        db.delete_column('fincas_servizoforestal', 'tipo_id')

        # Changing field 'ServizoForestal.final'
        db.alter_column('fincas_servizoforestal', 'final', self.gf('django.db.models.fields.DateField')())

        # Deleting field 'Finca.concello'
        db.delete_column('fincas_finca', 'concello_id')

        # Changing field 'Finca.ha_prado'
        db.alter_column('fincas_finca', 'ha_prado', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'Finca.lugar'
        db.alter_column('fincas_finca', 'lugar_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fincas.Lugar']))

        # Changing field 'Finca.zona'
        db.alter_column('fincas_finca', 'zona', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Finca.obs'
        db.alter_column('fincas_finca', 'obs', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Finca.ha_matorral'
        db.alter_column('fincas_finca', 'ha_matorral', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'Finca.codigo_ref'
        db.alter_column('fincas_finca', 'codigo_ref', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Finca.fecha_plantacion'
        db.alter_column('fincas_finca', 'fecha_plantacion', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Finca.ha_total'
        db.alter_column('fincas_finca', 'ha_total', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'Finca.ha_construidas'
        db.alter_column('fincas_finca', 'ha_construidas', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'Finca.densidad'
        db.alter_column('fincas_finca', 'densidad', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'Finca.superficie'
        db.alter_column('fincas_finca', 'superficie', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Finca.agregado'
        db.alter_column('fincas_finca', 'agregado', self.gf('django.db.models.fields.IntegerField')())


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
            'superficie': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
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
        'fincas.servizoforestal': {
            'Meta': {'object_name': 'ServizoForestal'},
            'comezo': ('django.db.models.fields.DateField', [], {}),
            'final': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fincas.ServizoForestalTipo']"})
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
