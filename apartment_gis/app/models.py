from django.contrib.gis.db import models
from django.contrib import admin

class Apartment(models.Model):
    address = models.CharField(max_length=200)
    district = models.CharField(max_length=50)
    rooms_num = models.IntegerField(default=1)
    month_price = models.IntegerField()
    floor = models.IntegerField()
    storeys_num = models.IntegerField()
    description = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=50)
    location = models.PointField()
    objects = models.GeoManager()

    def __unicode__(self):
        return self.address

    class Meta:
        unique_together = ('address', 'rooms_num', 'month_price', 'floor',)

class NurserySchool(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=50)
    location = models.PointField()
    objects = models.GeoManager()


    def __unicode__(self):
        return self.name