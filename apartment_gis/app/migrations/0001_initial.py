# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Apartment'
        db.create_table(u'app_apartment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('district', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('rooms_num', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('month_price', self.gf('django.db.models.fields.IntegerField')()),
            ('floor', self.gf('django.db.models.fields.IntegerField')()),
            ('storeys_num', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal(u'app', ['Apartment'])

        # Adding unique constraint on 'Apartment', fields ['address', 'rooms_num', 'month_price', 'floor']
        db.create_unique(u'app_apartment', ['address', 'rooms_num', 'month_price', 'floor'])

        # Adding model 'NurserySchool'
        db.create_table(u'app_nurseryschool', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal(u'app', ['NurserySchool'])


    def backwards(self, orm):
        # Removing unique constraint on 'Apartment', fields ['address', 'rooms_num', 'month_price', 'floor']
        db.delete_unique(u'app_apartment', ['address', 'rooms_num', 'month_price', 'floor'])

        # Deleting model 'Apartment'
        db.delete_table(u'app_apartment')

        # Deleting model 'NurserySchool'
        db.delete_table(u'app_nurseryschool')


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
        u'app.nurseryschool': {
            'Meta': {'object_name': 'NurserySchool'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['app']