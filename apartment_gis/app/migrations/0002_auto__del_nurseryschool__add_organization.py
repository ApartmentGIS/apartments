# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'NurserySchool'
        db.delete_table(u'app_nurseryschool')

        # Adding model 'Organization'
        db.create_table(u'app_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal(u'app', ['Organization'])


    def backwards(self, orm):
        # Adding model 'NurserySchool'
        db.create_table(u'app_nurseryschool', (
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'app', ['NurserySchool'])

        # Deleting model 'Organization'
        db.delete_table(u'app_organization')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['app']