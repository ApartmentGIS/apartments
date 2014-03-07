# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point, fromstr

from app.models import Apartment
import csv
import os

class Command(BaseCommand):
    args = ''
    help = 'Add parsed data from domchel.ru to database'

    def handle(self, *args, **options):
        apt = Apartment()
        data_filename = os.getcwd() + '/app/apartment_data_coord.csv'
        with open(data_filename, 'rb') as csv_read:
            r = csv.reader(csv_read, delimiter='#', quotechar='"')
            for row in r:
                a = Apartment(
                    address=row[0],
                    district=row[1],
                    rooms_num=row[2],
                    month_price=row[3],
                    floor=row[4],
                    storeys_num=row[5],
                    description=row[6],
                    phone_number=row[7],
                    location= fromstr("POINT(%s)" % (row[8])))
                try:
                    a.save()
                except:
                    print '! This apartment is already in database !'
                    continue
        csv_read.close()