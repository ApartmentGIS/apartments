# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point, fromstr
from optparse import make_option
from app.models import Apartment, NurserySchool
import csv
import os

class Command(BaseCommand):
    args = ''
    help = 'Add parsed data into database'
    option_list = BaseCommand.option_list + (
        make_option(
            "--apt_file",
            dest = "apartment_filename",
            help = "specify import file with apartment data",
            metavar = "FILE"
        ),
    )
    option_list = option_list + (
        make_option(
            "--school_file",
            dest = "school_filename",
            help = "specify import file with nursery school data",
            metavar = "FILE"
        ),
    )

    def handle(self, *args, **options):
        if(options['apartment_filename']):
            data_filename = os.getcwd() + '/app/'+options['apartment_filename']

            with open(data_filename, 'rb') as csv_read:
                read_data = csv.reader(csv_read, delimiter='#', quotechar='"')
                for row in read_data:
                    apt = Apartment(
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
                        apt.save()
                    except:
                       print 'Error: This apartment is already in database'
                       continue
            csv_read.close()
        elif(options['school_filename']):
            data_filename = os.getcwd() + '/app/'+options['school_filename']
            with open(data_filename, 'rb') as csv_read:
                read_data = csv.reader(csv_read, delimiter='#', quotechar='"')
                for row in read_data:
                    ns = NurserySchool(
                        name=row[0],
                        address=row[1],
                        phone_number=row[2],
                        location= fromstr("POINT(%s)" % (row[3])))
                    try:
                        ns.save()
                    except:
                        print 'Error: This school is already in database'
                        continue
            csv_read.close()
        else:
            raise CommandError("One of the options `--apt_file=...` or `--school_file` must be specified.")

