# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Organization', fields ['name']
        db.create_unique(u'app_organization', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Organization', fields ['name']
        db.delete_unique(u'app_organization', ['name'])


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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['app']