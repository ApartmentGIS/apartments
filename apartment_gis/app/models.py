from django.contrib.gis.db import models

class Apartment(models.Model):
	address = models.CharField(max_length = 200)
	district = models.CharField(max_length = 50)
	rooms_num = models.IntegerField(default = 1)
	month_price = models.IntegerField()
	floor = models.IntegerField()
	storeys_num = models.IntegerField()
	description = models.CharField(max_length = 500)
	location = models.PointField()
	objects = models.GeoManager()