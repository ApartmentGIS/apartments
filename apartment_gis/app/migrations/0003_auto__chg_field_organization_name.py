# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.core.management import call_command

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Changing field 'Organization.name'
        db.alter_column(u'app_organization', 'name', self.gf('django.db.models.fields.CharField')(max_length=150))

        call_command('data_import', org_filename='organizations.csv')

    def backwards(self, orm):
        # Changing field 'Organization.name'
        db.alter_column(u'app_organization', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        u'app.apartment': {
            'Meta': {'unique_together': "(('address', 'rooms_num', 'month_price', 'floor'),)", 'object_name': 'Apartment'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'floor': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'month_price': ('django.db.models.fields.IntegerField', [], {}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rooms_num': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'storeys_num': ('django.db.models.fields.IntegerField', [], {})
        },
        u'app.organization': {
            'Meta': {'object_name': 'Organization'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['app']