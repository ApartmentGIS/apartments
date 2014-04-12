# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point, fromstr
from optparse import make_option
from app.models import Apartment, Organization
import csv
import os


class Command(BaseCommand):
    args = ''
    help = 'Add parsed data into database'
    option_list = BaseCommand.option_list + (
        make_option(
            "--apt_filename",
            dest="apt_filename",
            help="specify importing file with apartment data",
            metavar="FILE"
        ),
    )
    option_list = option_list + (
        make_option(
            "--org_filename",
            dest="org_filename",
            help="specify import file with organizations data",
            metavar="FILE"
        ),
    )

    def handle(self, *args, **options):
        if options['apt_filename']:
            data_filename = os.getcwd() + '/app/'+options['apt_filename']

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
                        location=fromstr("POINT(%s)" % (row[8])))
                    try:
                        apt.save()
                    except Exception as error:
                        print "ERROR: %s" % error
                        continue
            csv_read.close()
        elif options['org_filename']:
            data_filename = os.getcwd() + '/app/'+options['org_filename']
            with open(data_filename, 'rb') as csv_read:
                read_data = csv.reader(csv_read, delimiter='#', quotechar='"')
                for row in read_data:
                    org_type = row[0]
                    if org_type == 'Детские сады / Ясли':
                        org = Organization(
                            type='KIN',
                            name=row[1],
                            address=row[2],
                            location=fromstr("POINT(%s)" % (row[3])))
                    elif org_type == 'школы':
                        org = Organization(
                             type='SCH',
                             name=row[1],
                             address=row[2],
                             location=fromstr("POINT(%s)" % (row[3])))
                    elif org_type == 'университеты':
                          org = Organization(
                              type='UNI',
                              name=row[1],
                              address=row[2],
                              location=fromstr("POINT(%s)" % (row[3])))
                    elif org_type == 'больницы':
                        org = Organization(
                            type='HOS',
                            name=row[1],
                            address=row[2],
                            location=fromstr("POINT(%s)" % (row[3])))
                    elif org_type == 'фитнес-клубы':
                        org = Organization(
                            type='FIT',
                            name=row[1],
                            address=row[2],
                            location=fromstr("POINT(%s)" % (row[3])))
                    else:
                        org = Organization(
                            type='SHP',
                            name=row[1],
                            address=row[2],
                            location=fromstr("POINT(%s)" % (row[3])))
                    try:
                        org.save()
                    except Exception as error:
                        print "ERROR: %s" % error
                        continue
                csv_read.close()
        else:
            raise CommandError("One of the options `--apt_filename=...` or `--org_filename` must be specified.")

